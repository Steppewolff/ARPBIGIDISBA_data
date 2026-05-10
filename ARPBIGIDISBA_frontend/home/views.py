from django.apps import apps
from django.db.models import ForeignKey, Q
from django.shortcuts import render, redirect
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView
from import_export.admin import ExportMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import re
import pandas as pd

from .models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, BreakpointTable, Hospital, SampleType
from .tables import CombinedTable, create_mic_table # MicTable
from .forms import HospitalForm, MicForm, MetadataGeneralForm, FenotipoForm, SequenceAnalysisForm, MetadataClinicForm
from .filters import MultiFilter

class MyLoginView(LoginView):
    template_name = 'login.html'

# Create your views here.
# @login_required
def home(request):
    return render(request, 'home.html')



# @login_required
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

class ResultadosListView(ExportMixin, SingleTableMixin, FilterView): #LoginRequiredMixin,
    table_class = CombinedTable
    model = MetadataGeneral
    template_name = 'resultados.html'
    filterset_class = MultiFilter

    # Presets for custom exportations
    column_presets = {"mepram_only": ["isolate_name", "species", "isolate_source", "isolation_date"],
                      "mic_only": ["isolate_name", "species", "isolation_date", "pip", "pip_clinical_category", "fep", "fep_clinical_category", "caz", "caz_clinical_category", "ctz", "ctz_clinical_category", "imi", "imi_clinical_category", "mer", "mer_clinical_category", "azt", "azt_clinical_category", "cip", "cip_clinical_category"],
                      "all": None}

    def mra_classification(self):
        pass

    def create_export(self, export_format):
        # Crear la tabla (con filtros/applicable queryset)
        table = self.get_table(**self.get_table_kwargs())

        # Leer excluded_columns desde GET (plugin añade excluded_columns=col1,col2)
        excluded_param = self.request.GET.get('excluded_columns', '')
        if excluded_param:
            raw = [c.strip() for c in excluded_param.split(',') if c.strip()]
        else:
            raw = []

        # Validar y normalizar contra los nombres reales de columnas de la tabla
        all_cols = list(table.columns.names())
        exclude = [c for c in raw if c in all_cols]

        # Crear exporter pasando exclude_columns (si exclude está vacío pasar None)
        exclude_arg = exclude if exclude else None
        exporter = TableExport(export_format, table=table, exclude_columns=exclude_arg)

        return exporter

    def get_context_data(self, **kwargs):
        verbose_used = self.request.session.get('verbose_used', {})
        context = super().get_context_data(**kwargs)

        # Obtener los datos para la tabla de Mic con isolate_name
        filtered_ids = self.get_queryset().values_list('isolate_id', flat=True)
        # qs_mic = Mic.objects.select_related("matadatageneral.isolate_name").all()
        # qs_mic = list(Mic.objects.select_related("isolate_id").filter(isolate_id__in=filtered_ids))
        # context['qs_mic'] = qs_mic
        # # Sin breakpoints seleccionados aún: tabla vacía con cabeceras genéricas
        # DefaultMicTable = create_mic_table()
        # context['mic_table'] = DefaultMicTable(data=qs_mic)
        # RequestConfig(self.request).configure(context['mic_table'])

        qs_mic = list(Mic.objects.select_related("isolate_id").filter(isolate_id__in=filtered_ids))
        context['qs_mic'] = qs_mic

        selected_table_1 = self.request.GET.get('breakpoint_table_1') or None
        selected_table_2 = self.request.GET.get('breakpoint_table_2') or None

        alias_1 = self.request.GET.get('alias_1') or 'CC1'
        alias_2 = self.request.GET.get('alias_2') or 'CC2'

        if selected_table_1 or selected_table_2:
            bp_dict_1 = self._get_bp_dict(selected_table_1)
            bp_dict_2 = self._get_bp_dict(selected_table_2)
            self._apply_clinical_categories(qs_mic, bp_dict_1, bp_dict_2)
            DynamicMicTable = create_mic_table(
                label1=alias_1,
                label2=alias_2,
            )
            context['mic_table'] = DynamicMicTable(data=qs_mic)
        else:
            context['mic_table'] = create_mic_table()(data=qs_mic)

        RequestConfig(self.request).configure(context['mic_table'])

        context['selected_table_1'] = selected_table_1
        context['selected_table_2'] = selected_table_2
        context['alias_1'] = alias_1
        context['alias_2'] = alias_2
        context['selected_filepath_1'] = self._get_filepath(selected_table_1)
        context['selected_filepath_2'] = self._get_filepath(selected_table_2)
        context['breakpoints_tables'] = BreakpointTable.objects.all().values_list('table_version_name', flat=True)

        context['filter'] = self.get_filterset(self.get_filterset_class())
        context['verbose_used'] = verbose_used

        # Garantizar que 'table' siempre esté presente
        if 'table' not in context or not hasattr(context['table'], 'columns'):
            context['table'] = self.get_table()

        # Añadir filtros de la vista filtrada para que aparezcan en /results
        verbose_used = context.get('verbose_used', {}).copy()
        # for key, value in self.request.GET.items():
        #     if key in ['csrfmiddlewaretoken', 'page'] or not value:
        #         continue
        #     verbose_used[key.replace('_', ' ').capitalize()] = value

        for key in self.request.GET.keys():
            if key in ['csrfmiddlewaretoken', 'page']:
                continue
            values = [v for v in self.request.GET.getlist(key) if v]
            if not values:
                continue
            if key in ('incluir', 'excluir'):
                label = 'Include' if key == 'incluir' else 'Exclude'
                # Construir mapa mutacion -> gen desde OPCIONES_FILTRO
                gen_map = {}
                for gen, subchoices in MultiFilter.OPCIONES_FILTRO:
                    for mut, _ in subchoices:
                        gen_map[mut] = gen
                # Agrupar mutaciones seleccionadas por gen
                gen_groups = {}
                for mut in values:
                    gen = gen_map.get(mut, 'Unknown')
                    gen_groups.setdefault(gen, []).append(mut)
                # Formato: PA0004 (D4N, S466Y, A103G), PA0315 (K44M)
                display = ', '.join(
                    f"{gen} ({', '.join(muts)})"
                    for gen, muts in sorted(gen_groups.items())
                )
                verbose_used[label] = display
            else:
                verbose_used[key.replace('_', ' ').capitalize()] = values[0]

        context['verbose_used'] = verbose_used
        context['breakpoints_tables'] = BreakpointTable.objects.all().values_list('table_version_name', flat=True)

        return context

    def get_table(self, **kwargs):
        # qs=self.get_queryset()
        qs = getattr(self, 'object_list', self.get_queryset())
        table = self.table_class(data=qs, request=self.request, **kwargs)
        RequestConfig(self.request).configure(table)

        return table

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('_export', None)
        export_mic_format = request.GET.get('_export_mic', None)
        preset = request.GET.get('preset', None)

        # If the get request has a preset variable, export only those columns
        if preset and TableExport.is_valid_format(export_format):
            # table = self.get_table()
            filterset = self.get_filterset(self.get_filterset_class())
            self.object_list = filterset.qs
            table = self.get_table()
            visible_columns = self.column_presets.get(preset, None)
            if visible_columns is None:
                return HttpResponseBadRequest("Preset not found ")

            all_cols = list(table.columns.names())
            exclude = [c for c in all_cols if c not in visible_columns]

            exporter = TableExport(export_format, table, exclude_columns=(exclude if exclude else None))
            return exporter.response(f'arpbig_data_export_{preset}.{export_format}')

        # Exportation of the whole table (CombinedTable)
        if TableExport.is_valid_format(export_format):
            # table = self.get_table()
            filterset = self.get_filterset(self.get_filterset_class())
            self.object_list = filterset.qs
            table = self.get_table()
            # exporter = TableExport(export_format, table)
            excluded_columns_param = self.request.GET.get('excluded_columns', '')  # cadena vacía si no existe
            excluded_columns = excluded_columns_param.split(',') if excluded_columns_param else None

            exporter = TableExport(export_format, table, exclude_columns=excluded_columns)
            return exporter.response('arpbig_data_export.{}'.format(export_format))

        # Exporta la tabla de MIC (mic_table)
        elif TableExport.is_valid_format(export_mic_format):
            # Reutilizamos la lógica para obtener el queryset de MIC, igual que en get_context_data
            # Retrieve last-used breakpoint table labels from session so the
            # export column headers match what the user sees on screen.
            t1 = request.session.get('selected_table_1') or 'BP Version 1'
            t2 = request.session.get('selected_table_2') or 'BP Version 2'

            filtered_ids = self.get_queryset().values_list('isolate_id', flat=True)
            qs_mic = Mic.objects.select_related("isolate_id").filter(isolate_id__in=filtered_ids)

            # Re-compute clinical categories if breakpoint tables are stored in session
            bp_dict_1 = self._get_bp_dict(t1 if t1 != 'BP Version 1' else None)
            bp_dict_2 = self._get_bp_dict(t2 if t2 != 'BP Version 2' else None)
            self._apply_clinical_categories(qs_mic, bp_dict_1, bp_dict_2)

            ExportMicTable = create_mic_table(label1=t1, label2=t2)
            mic_table = ExportMicTable(data=qs_mic)
            RequestConfig(self.request).configure(mic_table)
            exporter = TableExport(export_mic_format, mic_table)
            return exporter.response('arpbig_data_export_mic.{}'.format(export_mic_format))

        return super().get(request, *args, **kwargs)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_bp_dict(self, table_name):
        """Return the mic_breakpoints dict for *table_name*, or {} if absent."""
        if not table_name:
            return {}
        qs = BreakpointTable.objects.filter(table_version_name=table_name).values_list('mic_breakpoints', flat=True)
        return qs.first() or {}

    def _get_filepath(self, table_name):
        """Return the filepath of the BreakpointTable row, or None."""
        if not table_name:
            return None
        obj = BreakpointTable.objects.filter(table_version_name=table_name).first()
        return obj.filepath if obj else None

    def _apply_clinical_categories(self, qs_mic, bp_dict_1, bp_dict_2):
        """
        Inject {ab}_clinical_category_1 and {ab}_clinical_category_2 attributes
        onto each record in *qs_mic* in-place, using the two breakpoint dicts.
        """
        all_abs = set(bp_dict_1.keys()) | set(bp_dict_2.keys())
        for record in qs_mic:
            for ab in all_abs:
                value = getattr(record, ab, None)
                if value is None:
                    continue

                # ---- Breakpoint table 1 ----
                if ab in bp_dict_1:
                    bp = bp_dict_1[ab]
                    if bp and (None in bp.values() or "-" in bp.values()):
                        setattr(record, f"{ab}_clinical_category_1", "Sin BP")
                    elif bp:
                        setattr(
                            record, f"{ab}_clinical_category_1",
                            self.compute_clinical_category(value, bp))

                # ---- Breakpoint table 2 ----
                if ab in bp_dict_2:
                    bp = bp_dict_2[ab]
                    if bp and (None in bp.values() or "-" in bp.values()):
                        setattr(record, f"{ab}_clinical_category_2", "Sin BP")
                    elif bp:
                        setattr(
                            record, f"{ab}_clinical_category_2",
                            self.compute_clinical_category(value, bp))

    def compute_clinical_category(self, value, bp):
        """
        value: el valor real (numérico o cadena) obtenido del registro para el antibiótico.
        bp: un diccionario con al menos las claves "S" y "R". Por ejemplo: {"R": 16, "S": 0.001}
        """
        comparator = None

        # Si el valor es None (null) o no está definido
        if value is None:
            return "NA"
        # Si el valor es exactamente el guión (string)
        if isinstance(value, str) and value.strip() == "-":
            return "-"
        # Si el valor es la cadena "IE"
        if isinstance(value, str) and value.upper() == "IE":
            return "IE"
        try:
            valor = float(value)
        except (TypeError, ValueError):
            # Expresión regular para detectar comparadores (<, <=, >, >=) y extraer el número
            match = re.match(r'^(<|<=|≤|>|>=|≥)?\s*(\d*\.?\d+)$', str(value).strip())
            if match:
                comparator, number = match.groups()
                if comparator == "≤":
                    comparator = "<="
                if comparator == "≥":
                    comparator = ">="

                try:
                    valor = float(number)
                except (TypeError, ValueError):
                    return "NA"
            else:
                try:
                    valor = float(value)
                    comparator = None  # Sin operador
                except (TypeError, ValueError):
                    return "NA"

        # Se asume que los breakpoints vienen definidos numéricamente (aunque puede ser string en algunos casos)
        s_bp = bp.get("S")
        r_bp = bp.get("R")

        try:
            s_bp = float(s_bp)
        except (TypeError, ValueError):
            s_bp = None

        try:
            r_bp = float(r_bp)
        except (TypeError, ValueError):
            r_bp = None

        if comparator is None:
            if s_bp is not None and valor <= s_bp:
                return "S"
            elif r_bp is not None and valor > r_bp:
                return "R"
            else:
                return "I"

        elif comparator is not None:

            if s_bp is not None and (comparator == "<=" or comparator == "<") and valor <= s_bp:
                return "S"
            elif s_bp is not None and comparator == "<" and (valor/s_bp) == 2:
                return "S!"


            if r_bp is not None and (comparator == ">=" or comparator == ">") and valor > r_bp:
                return "R"
            elif r_bp is not None and comparator == ">" and (valor/r_bp) == 0.5:
                return "R!"


            if s_bp is not None and valor > s_bp and r_bp is not None and valor < r_bp:
                return "I"

        # En caso intermedio, se puede asignar "IE" u otro valor según tu criterio
        return "No se ha podido asignar valor S/I/R"

    def post(self, request, *args, **kwargs):
        self.update_parameters(request)
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        return render(request, 'resultados.html', context=context)

    def update_parameters(self, request, *args, **kwargs):
        parameters = request.POST.copy()
        parameters_used = {}  # ← empezar vacío siempre
        verbose_used = {}  # ← empezar vacío siempre

        for parameter, value in parameters.items():
            if parameter == 'csrfmiddlewaretoken' or value in ('', 'none'):
                continue
            for model in apps.get_models():
                for field in model._meta.get_fields():
                    if field.name == parameter:
                        new_name = field.verbose_name.capitalize()
                        parameters_used[field.name] = value
                        verbose_used[str(new_name)] = value
                        if isinstance(field, ForeignKey):
                            model_id = field.related_model._meta.pk.name
                            display_value = field.related_model.objects.get(
                                Q((model_id, value))
                            ).__str__()
                            verbose_used[str(new_name)] = display_value
                        break

        request.session['parameters_used'] = parameters_used
        request.session['verbose_used'] = verbose_used
        request.session.modified = True


    # def update_parameters(self, request, *args, **kwargs):
    #     parameters = request.POST.copy()
    #     # parameters = (request.POST if request.method == "POST" else request.GET).copy()
    #     parameters_used = request.session.get('parameters_used', {})
    #     verbose_used = request.session.get('verbose_used', {})
    #     # for parameter, value in parameters.items():
    #
    #     for parameter in set(parameters.keys()):
    #         values = [v for v in parameters.getlist(parameter) if v and v != 'none']
    #         if not values or parameter == 'csrfmiddlewaretoken':
    #             continue
    #         value = values[0]  # para el filtrado se sigue usando el primer valor
    #         if parameter == 'csrfmiddlewaretoken' or value == 'none':
    #             pass
    #         elif value == '' :
    #             if parameter in parameters_used:
    #                 parameters_used.pop(parameter)
    #                 for model in apps.get_models():
    #                     for field in model._meta.get_fields():
    #                         if field.name == parameter:
    #                             new_name = field.verbose_name.capitalize()
    #                             verbose_used.pop(new_name, None)
    #                             break
    #             else:
    #                 pass
    #         else:
    #             for model in apps.get_models():
    #                 for field in model._meta.get_fields():
    #                     if field.name == parameter:
    #                         new_name = field.verbose_name.capitalize()
    #                         parameters_used[field.name] = value
    #                         verbose_used[str(new_name)] = ', '.join(values)
    #                         if isinstance(field, ForeignKey):
    #                             model_id = field.related_model._meta.pk.name
    #                             value = field.related_model.objects.get(Q((model_id, value))).__str__()
    #                             verbose_used[str(new_name)] = ', '.join(values)
    #
    #                         break
    #
    #     self.request.session['parameters_used'] = parameters_used
    #     self.request.session['verbose_used'] = verbose_used
    #     self.request.session.modified = True

    def get_queryset(self, *args, **kwargs):
        qs = super(ResultadosListView, self).get_queryset(*args, **kwargs)
        metadatageneral_fields=[field.name for field in MetadataGeneral._meta.get_fields()]
        # self.update_parameters(self.request)
        filter_param = self.request.session.get('parameters_used', {})
        for filter, value in filter_param.items():
            if filter not in ['encoding', 'csrfmiddlewaretoken', '__len__'] and value != '':

                if filter in metadatageneral_fields:
                    kwargs_filter = {f'{filter}': value}

                else:
                    for model in apps.get_models():
                        if filter in [field.name for field in model._meta.get_fields()]:
                            filter_model = model.__name__.lower()
                            break

                    if 'comparison_' in str(filter):
                        filter_name = filter.replace('comparison_', '')
                        kwargs_filter = {f'{filter_model}__{filter_name}__{value}': filter_param.get(filter_name)}

                    elif filter_model in metadatageneral_fields:
                        kwargs_filter = {f'{filter_model}__{filter}': value}

                    else:
                        kwargs = {f'metadataclinic__{filter_model}__{filter}': value}

                qs = qs.filter(**kwargs_filter)

        qs = qs.filter().order_by("isolate_name")

        return qs

# def amr_clas_modal(request):
#     breakpoints_tables = BreakpointTable.objects.all().values_list('table_version_name', flat=True)
#     if request.method == "POST":
#         selected_table = request.POST.get('breakpoint_table')
#         selected_breakpoints = BreakpointTable.objects.filter(table_version_name=selected_table).values_list('mic_breakpoints')
#         return render(request, 'resultados.html', {"breakpoints_tables" : breakpoints_tables, "selected_table" : selected_table, 'selected_breakpoints':selected_breakpoints})
#
#     else:
#         return render(request, 'amr_clas_modal.html', {"breakpoints_tables" : breakpoints_tables})

def pipelines(request):
    return render(request, 'pipelines.html')


def documentacion(request):
    return render(request, 'documentacion.html')


# @login_required
def cargadatos(request):
    return render(request, 'cargadatos.html')


def contacto(request):
    return render(request, 'contacto.html')
