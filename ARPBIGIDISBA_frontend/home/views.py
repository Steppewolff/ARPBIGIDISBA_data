from django.apps import apps
from django.db.models import ForeignKey, Q
from django.shortcuts import render, redirect
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView
import pandas as pd

from .models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, BreakpointTable, Hospital, SampleType
from .tables import CombinedTable
from .forms import HospitalForm, MicForm, MetadataGeneralForm, FenotipoForm, SequenceAnalysisForm, MetadataClinicForm
from .filters import MultiFilter


# Create your views here.
def home(request):
    return render(request, 'home.html')

def busqueda(request):
    if request.method == 'POST':
        metadatageneral_form = MetadataGeneralForm(request.POST)
        metadataclinic_form = MetadataClinicForm(request.POST)
        hospital_form = HospitalForm(request.POST)
        mic_form = MicForm(request.POST)
        fenotipo_form = FenotipoForm(request.POST)
        secuencia_analisis_form = SequenceAnalysisForm(request.POST)

        if metadatageneral_form.is_valid() and hospital_form.is_valid() and mic_form.is_valid() and fenotipo_form.is_valid() and secuencia_analisis_form.is_valid() and metadataclinic_form.is_valid():
            return render(request, 'resultados.html')

    else:
        metadatageneral_form = MetadataGeneralForm()
        metadataclinic_form = MetadataClinicForm()
        hospital_form = HospitalForm()
        mic_form = MicForm()
        fenotipo_form = FenotipoForm()
        secuencia_analisis_form = SequenceAnalysisForm()

        return render(request, 'busqueda.html',
                      {'metadatageneral_form': metadatageneral_form, 'metadataclinic_form': metadataclinic_form, 'hospital_form': hospital_form,
                       'mic_form': mic_form,
                       'fenotipo_form': fenotipo_form, 'secuencia_analisis_form': secuencia_analisis_form})

class ResultadosListView(SingleTableMixin, FilterView):
    table_class = CombinedTable
    model = MetadataGeneral
    template_name = 'resultados.html'
    filterset_class = MultiFilter

    def mra_classification(self):
        pass

    def get_context_data(self, **kwargs):
        verbose_used = self.request.session.get('verbose_used', {})
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filterset(self.get_filterset_class())
        context['verbose_used'] = verbose_used
        context['Mic_list'] = Mic.objects.all()

        return context

        context['FilePath_list'] = FilePath.objects.all()
        context['MetadataClinic_list'] = MetadataClinic.objects.all()
        context['PhenotypicData_list'] = PhenotypicData.objects.all()
        context['SequenceAnalysis_list'] = SequenceAnalysis.objects.all()
        context['SequencingInfo_list'] = SequencingInfo.objects.all()

        return context

    def get_table(self, **kwargs):
        qs=self.get_queryset()
        table = self.table_class(data=qs, **kwargs)

        RequestConfig(self.request).configure(table)
        return table

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('_export', None)

        if TableExport.is_valid_format(export_format):
            table = self.get_table()
            exporter = TableExport(export_format, table)
            return exporter.response('arpbig_data_export.{}'.format(export_format))

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        mra_classification_dict = {}

        return render(request, 'resultados.html', context=context)

    def update_parameters(self, request, *args, **kwargs):
        parameters = request.POST.copy()
        parameters_used = request.session.get('parameters_used', {})
        verbose_used = request.session.get('verbose_used', {})
        for parameter, value in parameters.items():
            if parameter == 'csrfmiddlewaretoken' or value == 'none':
                pass
            elif value == '' :
                if parameter in parameters_used:
                    parameters_used.pop(parameter)
                    for model in apps.get_models():
                        for field in model._meta.get_fields():
                            if field.name == parameter:
                                new_name = field.verbose_name.capitalize()
                                verbose_used.pop(new_name)
                                break
                else:
                    pass
            else:
                for model in apps.get_models():
                    for field in model._meta.get_fields():
                        if field.name == parameter:
                            new_name = field.verbose_name.capitalize()
                            parameters_used[field.name] = value
                            verbose_used[str(new_name)] = value
                            if isinstance(field, ForeignKey):
                                model_id = field.related_model._meta.pk.name
                                value = field.related_model.objects.get(Q((model_id, value))).__str__()
                                verbose_used[str(new_name)] = value

                            break

        self.request.session['parameters_used'] = parameters_used
        self.request.session['verbose_used'] = verbose_used

    def get_queryset(self, *args, **kwargs):
        qs = super(ResultadosListView, self).get_queryset(*args, **kwargs)
        metadatageneral_fields=[field.name for field in MetadataGeneral._meta.get_fields()]
        self.update_parameters(self.request)
        filter_param = self.request.session.get('parameters_used', {})
        for filter, value in filter_param.items():
            if filter not in ['encoding', 'csrfmiddlewaretoken', '__len__'] and value != '':

                if filter in metadatageneral_fields:
                    kwargs = {f'{filter}': value}

                else:
                    for model in apps.get_models():
                        if filter in [field.name for field in model._meta.get_fields()]:
                            filter_model = model.__name__.lower()
                            break

                    if 'comparison_' in str(filter):
                        filter_name = filter.replace('comparison_', '')
                        kwargs = {f'{filter_model}__{filter_name}__{value}': filter_param.get(filter_name)}

                    elif filter_model in metadatageneral_fields:
                        kwargs = {f'{filter_model}__{filter}': value}

                    else:
                        kwargs = {f'metadataclinic__{filter_model}__{filter}': value}

                qs = qs.filter(**kwargs)

        qs = qs.filter().order_by("isolate_name")

        return qs

def amr_clas_modal(request):
    breakpoints_tables = BreakpointTable.objects.all().values_list('table_version_name', flat=True)
    if request.method == "POST":
        selected_table = request.POST.get('breakpoint_table')
        selected_breakpoints = BreakpointTable.objects.filter(table_version_name=selected_table).values_list('mic_breakpoints')
        return render(request, 'amr_clas_modal.html', {"breakpoints_tables" : breakpoints_tables, "selected_table" : selected_table, 'selected_breakpoints':selected_breakpoints})

    else:
        return render(request, 'amr_clas_modal.html', {"breakpoints_tables" : breakpoints_tables})

def pipelines(request):
    return render(request, 'pipelines.html')


def documentacion(request):
    return render(request, 'documentacion.html')


def cargadatos(request):
    return render(request, 'cargadatos.html')


def contacto(request):
    return render(request, 'contacto.html')
