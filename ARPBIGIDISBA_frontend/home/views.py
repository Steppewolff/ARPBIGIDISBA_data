from django.apps import apps
from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableView, SingleTableMixin

from .models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, Hospital, SampleType
from .tables import MetadataGeneralTable, create_dynamic_table, CombinedTable
from .forms import HospitalForm, MicForm, MetadataGeneralForm, FenotipoForm, SequenceAnalysisForm, MetadataClinicForm


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


class ResultadosListView(SingleTableView):
    model = MetadataGeneral
    template_name = 'resultados.html'
    table_class = CombinedTable

    def get_context_data(self, **kwargs):
        context = super(ResultadosListView, self).get_context_data(**kwargs)



        context['FilePath_list'] = FilePath.objects.all()
        context['MetadataClinic_list'] = MetadataClinic.objects.all()
        context['Mic_list'] = Mic.objects.all()
        context['PhenotypicData_list'] = PhenotypicData.objects.all()
        context['SequenceAnalysis_list'] = SequenceAnalysis.objects.all()
        context['SequencingInfo_list'] = SequencingInfo.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)

        parameters = request.POST.copy()
        parameters_used = parameters.copy()
        for parameter, value in parameters.items():
            if parameter == 'csrfmiddlewaretoken' or value == '' or value == 'nome':
                parameters_used.pop(parameter)
            else:
                for model in apps.get_models():
                    for field in model._meta.get_fields():
                        # field_name = model._meta.get_field(parameter)
                        if field.name == parameter:
                            new_name = field.verbose_name
                            parameters_used[str(new_name)] = parameters_used.pop(parameter)

        context['parameters_used'] = parameters_used

        return render(request, 'resultados.html', context=context)

    def get_queryset(self, *args, **kwargs):
        qs = super(ResultadosListView, self).get_queryset(*args, **kwargs)
        metadatageneral_fields=[field.name for field in MetadataGeneral._meta.get_fields()]
        filters = self.request.POST.copy()
        for filter, value in filters.items():
            if filter not in ['encoding', 'csrfmiddlewaretoken', '__len__'] and value != '':

                if filter in metadatageneral_fields:
                    kwargs = {f'{filter}': value}

                else:
                    # isolate_ids = self.get_context_data().get(filter)
                    for model in apps.get_models():
                        if filter in [field.name for field in model._meta.get_fields()]:
                            filter_model = model.__name__.lower()
                            break
                        else:
                            print(f'The field {filter} is not present in {model} model')

                    if 'comparison_' in str(filter):
                        filter_name = filter.replace('comparison_', '')
                        kwargs = {f'{filter_model}__{filter_name}__{value}': filters.get(filter_name)}

                    else:
                        kwargs = {f'{filter_model}__{filter}': value}


                qs = qs.filter(**kwargs)

        qs = qs.filter().order_by("isolate_name")
        return qs


# class ResultadosTableView(SingleTableView):
#     model = Mic
#     template_name = 'resultados.html'
#     table_class = MicTable
#
#     # if request.method == 'POST':
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
#     def get_queryset(self, *args, **kwargs):
#         qs = super(ResultadosTableView, self).get_queryset(*args, **kwargs)
#         qs = qs.order_by("mic_id")
#         return qs


def pipelines(request):
    return render(request, 'pipelines.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def documentacion(request):
    return render(request, 'documentacion.html')


def cargadatos(request):
    return render(request, 'cargadatos.html')


def contacto(request):
    return render(request, 'contacto.html')
