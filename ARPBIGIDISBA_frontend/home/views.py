from django.apps import apps
from django.db.models import ForeignKey, Q
from django.shortcuts import render, redirect
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView
from import_export.admin import ExportMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import re
from functools import lru_cache
import pandas as pd

from .models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, BreakpointTable, Hospital, SampleType, InterestGenes
from .tables import CombinedTable, create_mic_table # MicTable
from .forms import HospitalForm, MicForm, MicSearchForm, MetadataGeneralForm, FenotipoForm, SequenceAnalysisForm, MetadataClinicForm
from .filters import MultiFilter
from django.db.models.signals import post_save
from django.dispatch import receiver

LOCUS_RE = re.compile(r'^(PA(?:LES|14)?[_ ]?\d{4,5})', re.IGNORECASE)

def _extract_locus(key):
    m = LOCUS_RE.match(key)
    return m.group(1) if m else key

@lru_cache(maxsize=1)
def _get_locus_display_map():
    """Returns {locus: name} from InterestGenes. Uses synonym_name if official_name is empty."""
    result = {}
    for ig in InterestGenes.objects.exclude(locus=None).values('locus', 'official_name', 'synonym_name'):
        if not ig['locus']:
            continue
        name = (ig['official_name'] or ig['synonym_name'] or '').strip()
        result[ig['locus']] = name
    return result

@receiver(post_save, sender=InterestGenes)
def _clear_locus_display_cache(sender, **kwargs):
    _get_locus_display_map.cache_clear()

class MyLoginView(LoginView):
    template_name = 'login.html'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def _get_all_genes(sa_qs=None):
    """Sorted list of unique gene keys from mutational_resistome_muts.
    Pass a filtered SequenceAnalysis queryset or None for all records."""
    if sa_qs is None:
        sa_qs = SequenceAnalysis.objects.all()
    loci = set()
    for sa in sa_qs.exclude(mutational_resistome_muts=None).only('mutational_resistome_muts'):
        for key in (sa.mutational_resistome_muts or {}).keys():
            loci.add(_extract_locus(key))
    return sorted(loci)

def _get_genes_subset_map():
    """Dict {locus: [subset1, subset2, ...]} from the InterestGenes table.
    Used by the template to enable subset-filter buttons on the gene selector."""
    result = {}
    for ig in InterestGenes.objects.exclude(locus=None).values('locus', 'subset'):
        locus = (ig['locus'] or '').strip()
        if not locus:
            continue
        raw = ig['subset'] or []
        # MultiSelectField returns a list; guard in case a string arrives (e.g. from a fixture)
        if isinstance(raw, str):
            subsets = [s.strip() for s in raw.split(',') if s.strip()]
        else:
            subsets = [s.strip() for s in raw if s]
        result[locus] = subsets
    return result

def busqueda(request):
    return render(request, 'busqueda.html', {
        'metadatageneral_form':    MetadataGeneralForm(),
        'metadataclinic_form':     MetadataClinicForm(),
        'hospital_form':           HospitalForm(),
        'mic_form':                MicForm(),
        'mic_search_form':         MicSearchForm(),
        'fenotipo_form':           FenotipoForm(),
        'secuencia_analisis_form': SequenceAnalysisForm(),
        'all_genes':               _get_all_genes(),
        'all_genes_display': [
            (g, f"{g} ({_get_locus_display_map().get(g, '')})" if _get_locus_display_map().get(g) else g)
            for g in _get_all_genes()
        ],
        'genes_subset_map': json.dumps(_get_genes_subset_map()),
    })


def _get_gene_category(gene, muts_json, pols_json):
    """WT | Mutation | Polymorphism | Both — compares muts vs pols JSON for a single gene."""
    def _lookup(json_dict, locus):
        if not json_dict:
            return 'WT'
        if locus in json_dict:
            return json_dict[locus]
        return next((v for k, v in json_dict.items() if _extract_locus(k) == locus), 'WT')

    def variants(val):
        if not val:
            return set()
        return {v.strip() for v in val.split(';') if v.strip() and v.strip().upper() != 'WT'}

    muts_val = _lookup(muts_json, gene)
    pols_val  = _lookup(pols_json, gene)
    muts_v = variants(muts_val)
    pols_v = variants(pols_val)
    pol_only = pols_v - muts_v

    if muts_v and pol_only:
        return 'Both'
    if muts_v:
        return 'Mutation'
    if pol_only:
        return 'Polymorphism'
    return 'WT'

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
        # Build the table (with filters / applicable queryset)
        table = self.get_table(**self.get_table_kwargs())

        # Read excluded_columns from GET (plugin appends excluded_columns=col1,col2)
        excluded_param = self.request.GET.get('excluded_columns', '')
        if excluded_param:
            raw = [c.strip() for c in excluded_param.split(',') if c.strip()]
        else:
            raw = []

        # Validate and normalise against the real column names of the table
        all_cols = list(table.columns.names())
        exclude = [c for c in raw if c in all_cols]

        # Build exporter passing exclude_columns (pass None when exclude is empty)
        exclude_arg = exclude if exclude else None
        exporter = TableExport(export_format, table=table, exclude_columns=exclude_arg)

        return exporter

    def get(self, request, *args, **kwargs):
        """Intercepts the export response to set the download-progress cookie."""
        response = super().get(request, *args, **kwargs)
        token = request.GET.get('download_token', '')
        # Only add cookie if this is an export (Content-Disposition: attachment)
        if token and 'attachment' in response.get('Content-Disposition', ''):
            response.set_cookie(
                f'download_done_{token}', '1',
                max_age=60, path='/', samesite='Lax'
            )
        return response

    def get_context_data(self, **kwargs):
        verbose_used = self.request.session.get('verbose_used', {})
        context = super().get_context_data(**kwargs)

        filtered_ids = self.object_list.values_list('isolate_id', flat=True)

        selected_table_1 = self.request.GET.get('breakpoint_table_1') or None
        selected_table_2 = self.request.GET.get('breakpoint_table_2') or None
        alias_1 = self.request.GET.get('alias_1') or 'SIRv1'
        alias_2 = self.request.GET.get('alias_2') or 'SIRv2'

        qs_mic_qs = Mic.objects.select_related("isolate_id").filter(isolate_id__in=filtered_ids)
        mic_empty_cols = self._compute_mic_empty_columns(qs_mic_qs, selected_table_1, selected_table_2)

        if selected_table_1 or selected_table_2:
            bp_dict_1 = self._get_bp_dict(selected_table_1)
            bp_dict_2 = self._get_bp_dict(selected_table_2)
            qs_mic = list(qs_mic_qs)
            self._apply_clinical_categories(qs_mic, bp_dict_1, bp_dict_2)
            DynamicMicTable = create_mic_table(
                label1=alias_1, label2=alias_2, empty_columns=mic_empty_cols,
            )
        else:
            qs_mic = list(qs_mic_qs)
            DynamicMicTable = create_mic_table(empty_columns=mic_empty_cols)

        context['qs_mic'] = qs_mic
        context['mic_table'] = DynamicMicTable(data=qs_mic)
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

        # Ensure 'table' is always present in context
        if 'table' not in context or not hasattr(context['table'], 'columns'):
            context['table'] = self.get_table()

        for key in self.request.GET.keys():
            if key in ['csrfmiddlewaretoken', 'page']:
                continue
            values = [v for v in self.request.GET.getlist(key) if v]
            if not values:
                continue
            if key in ('incluir', 'excluir'):
                label = 'Include' if key == 'incluir' else 'Exclude'
                # Build mutation -> gene map from OPCIONES_FILTRO
                gen_map = {}
                for gen, subchoices in MultiFilter.OPCIONES_FILTRO:
                    for mut, _ in subchoices:
                        gen_map[mut] = gen
                # Group selected mutations by gene
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
            elif key == 'genes':
                verbose_used['Genes'] = ', '.join(values)
            elif key == 'loci_type':
                loci_labels = {
                    'muts': 'Mutations only',
                    'muts_pols': 'Mutations + Polymorphisms',
                }
                verbose_used['Loci type'] = loci_labels.get(values[0], values[0])
            else:
                verbose_used[key.replace('_', ' ').capitalize()] = values[0]

        context['verbose_used'] = verbose_used
        context['breakpoints_tables'] = BreakpointTable.objects.all().values_list('table_version_name', flat=True)

        # Resistome context
        loci_type     = self.request.GET.get('loci_type', '')
        selected_genes = [g for g in self.request.GET.getlist('genes') if g]
        show_heatmap  = self.request.GET.get('show_heatmap', 'no')
        filtered_ids = self.object_list.values_list('isolate_id', flat=True)
        sa_qs = SequenceAnalysis.objects.filter(isolate_id__in=filtered_ids)

        # Gene list from filtered records
        all_genes = _get_all_genes(sa_qs)
        _dmap = _get_locus_display_map()
        all_genes_display = [(g, f"{g} ({_dmap[g]})" if g in _dmap else g) for g in all_genes]

        # Warnings for missing JSON data
        resistome_warnings = []
        n_miss_muts = sa_qs.filter(mutational_resistome_muts=None).count()
        n_miss_pols = sa_qs.filter(mutational_resistome_pols=None).count()
        if n_miss_muts:
            resistome_warnings.append(
                f"{n_miss_muts} record(s) are missing mutation resistome data (mutational_resistome_muts). "
                f"Gene columns cannot be displayed for these records."
            )
        if n_miss_pols:
            resistome_warnings.append(
                f"{n_miss_pols} record(s) are missing polymorphism resistome data (mutational_resistome_pols). "
                f"Polymorphism calculation is not available for these records — "
                f"only mutation data will be used."
            )

        # Heatmap data for current page only
        heatmap_json = None
        if show_heatmap == 'yes' and selected_genes:
            table = context.get('table')
            if table and hasattr(table, 'page'):
                page_objects = [row.record for row in table.page.object_list]
            else:
                page_objects = list(self.get_queryset()[:25])
            page_ids = [obj.isolate_id for obj in page_objects]
            sa_page    = {sa.isolate_id_id: sa for sa in SequenceAnalysis.objects.filter(isolate_id__in=page_ids)}
            cat_map    = {'WT': 0, 'Mutation': 1, 'Polymorphism': 2, 'Both': 3}
            isolates, z_data, text_data = [], [], []
            for obj in page_objects:
                sa = sa_page.get(obj.isolate_id)
                if not sa:
                    continue
                muts = sa.mutational_resistome_muts or {}
                pols = sa.mutational_resistome_pols or {}
                isolates.append(obj.isolate_name or str(obj.isolate_id))
                z_data.append([cat_map[_get_gene_category(g, muts, pols)] for g in selected_genes])
                text_data.append([
                    f"Muts: {muts.get(g, 'WT')}<br>Pols: {pols.get(g, 'WT')}"
                    for g in selected_genes
                ])
            heatmap_json = json.dumps({
                'isolates': isolates, 'genes': selected_genes,
                'z': z_data, 'text': text_data,
            })

        context.update({
            'all_genes': all_genes,
            'all_genes_display': all_genes_display,
            'selected_genes':     selected_genes,
            'loci_type':          loci_type,
            'show_heatmap':       show_heatmap,
            'heatmap_json':       heatmap_json,
            'resistome_warnings': resistome_warnings,
        })

        context['per_page_options'] = [10, 25, 50, 100, 250]
        context['empty_cols_json'] = json.dumps(
            list(getattr(self, '_empty_cols', [])) + list(mic_empty_cols)
        )

        return context

    def get_table(self, **kwargs):
        from .tables import GeneColumn, create_dynamic_table
        qs = getattr(self, 'object_list', self.get_queryset())
        selected_genes = [g for g in self.request.GET.getlist('genes') if g]
        loci_type = self.request.GET.get('loci_type', 'muts')

        self._empty_cols = self._compute_empty_columns(qs)
        empty_cols = self._empty_cols

        if selected_genes:
            _dmap = _get_locus_display_map()
            gene_attrs = {
                f'gene_{gene}': GeneColumn(
                    gene_name=gene,
                    loci_type=loci_type,
                    verbose_name=mark_safe(f"{gene} (<em>{_dmap[gene]}</em>)") if gene in _dmap else gene
                )
                for gene in selected_genes
            }
            DynamicTable = create_dynamic_table(
                MetadataGeneral, MetadataClinic, Mic, PhenotypicData, SequenceAnalysis, FilePath,
                extra_columns=gene_attrs,
                empty_columns=empty_cols,
            )
        else:
            DynamicTable = create_dynamic_table(
                MetadataGeneral, MetadataClinic, Mic, PhenotypicData, SequenceAnalysis, FilePath,
                empty_columns=empty_cols,
            )

        table = DynamicTable(data=qs, request=self.request, **kwargs)

        try:
            per_page = int(self.request.GET.get('per_page', 25))
        except (ValueError, TypeError):
            per_page = 25
        RequestConfig(self.request, paginate={'per_page': per_page}).configure(table)
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
            excluded_columns_param = self.request.GET.get('excluded_columns', '')  # empty string if absent
            excluded_columns = excluded_columns_param.split(',') if excluded_columns_param else None

            exporter = TableExport(export_format, table, exclude_columns=excluded_columns)
            return exporter.response('arpbig_data_export.{}'.format(export_format))

        # Export the MIC table (mic_table)
        elif TableExport.is_valid_format(export_mic_format):
            # Reuse the same logic to obtain the MIC queryset as in get_context_data
            # Retrieve last-used breakpoint table labels from session so the
            # export column headers match what the user sees on screen.
            t1 = request.session.get('selected_table_1') or 'Breakpoint Version 1'
            t2 = request.session.get('selected_table_2') or 'Breakpoint Version 2'

            filterset = self.get_filterset(self.get_filterset_class())
            filtered_ids = filterset.qs.values_list('isolate_id', flat=True)
            qs_mic = Mic.objects.select_related("isolate_id").filter(isolate_id__in=filtered_ids)

            # Re-compute clinical categories if breakpoint tables are stored in session
            bp_dict_1 = self._get_bp_dict(t1 if t1 != 'Breakpoint Version 1' else None)
            bp_dict_2 = self._get_bp_dict(t2 if t2 != 'Breakpoint Version 2' else None)
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

    def _compute_empty_columns(self, qs):
        from django.db.models import Max, Field, JSONField as DJSONField, ForeignKey

        if not qs.exists():
            return set()

        empty = set()
        isolate_ids = qs.values_list('isolate_id', flat=True)

        mg_fields = [
            f for f in MetadataGeneral._meta.get_fields()
            if isinstance(f, Field) and not isinstance(f, (DJSONField, ForeignKey))
        ]
        try:
            agg = qs.aggregate(**{f.name: Max(f.name) for f in mg_fields})
            for f in mg_fields:
                if agg.get(f.name) in (None, '', '-'):
                    empty.add(f.name)
        except Exception:
            pass

        for model in [MetadataClinic, Mic, PhenotypicData, SequenceAnalysis, FilePath]:
            rel_fields = [
                f for f in model._meta.get_fields()
                if isinstance(f, Field)
                and not isinstance(f, (DJSONField, ForeignKey))
                and '_id' not in f.name          # mirrors create_dynamic_table exclusion
            ]
            if not rel_fields:
                continue
            try:
                rel_qs = model.objects.filter(isolate_id__in=isolate_ids)
                agg = rel_qs.aggregate(**{f.name: Max(f.name) for f in rel_fields})
                prefix = model._meta.model_name
                for f in rel_fields:
                    if agg.get(f.name) in (None, '', '-'):
                        empty.add(f'{prefix}_{f.name}')
            except Exception:
                pass

        return empty

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

                # Breakpoint table 1
                if ab in bp_dict_1:
                    bp = bp_dict_1[ab]
                    if bp and (None in bp.values() or "-" in bp.values()):
                        setattr(record, f"{ab}_clinical_category_1", "No Breakpoint")
                    elif bp:
                        setattr(
                            record, f"{ab}_clinical_category_1",
                            self.compute_clinical_category(value, bp))

                # Breakpoint table 2
                if ab in bp_dict_2:
                    bp = bp_dict_2[ab]
                    if bp and (None in bp.values() or "-" in bp.values()):
                        setattr(record, f"{ab}_clinical_category_2", "No Breakpoint")
                    elif bp:
                        setattr(
                            record, f"{ab}_clinical_category_2",
                            self.compute_clinical_category(value, bp))

    def compute_clinical_category(self, value, bp):
        """
        value: the actual value (numeric or string) obtained from the record for the antibiotic.
        bp: a dict with at least the keys "S" and "R". Example: {"R": 16, "S": 0.001}
        """
        comparator = None

        # If value is None (null) or undefined
        if value is None:
            return "NA"
        # If value is exactly a dash string
        if isinstance(value, str) and value.strip() == "-":
            return "-"
        # If value is the string "IE"
        if isinstance(value, str) and value.upper() == "IE":
            return "IE"
        try:
            valor = float(value)
        except (TypeError, ValueError):
            # Regex to detect comparators (<, <=, >, >=) and extract the number
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
                    comparator = None  # no comparator
                except (TypeError, ValueError):
                    return "NA"

        # Breakpoints are expected to be numeric (though they may arrive as strings in some cases)
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

        # Intermediate case — assign "IE" or another value as appropriate
        return "Could not assign S/I/R value"

    def _compute_mic_empty_columns(self, qs_mic, selected_table_1, selected_table_2):
        """
        Returns the set of MIC table column names to hide by default:
        - ab + ab_cc1 + ab_cc2  when the antibiotic field is entirely null.
        - all *_cc1 when no breakpoint table 1 is selected.
        - all *_cc2 when no breakpoint table 2 is selected.
        """
        from django.db.models import Max
        from .tables import MIC_ANTIBIOTICS

        empty = set()
        mic_field_names = {f.name for f in Mic._meta.get_fields()}

        if qs_mic.exists():
            try:
                valid_abs = [ab for ab in MIC_ANTIBIOTICS if ab in mic_field_names]
                agg = qs_mic.aggregate(**{ab: Max(ab) for ab in valid_abs})
                for ab in valid_abs:
                    if agg.get(ab) in (None, '', '-'):
                        empty.update([ab, f'{ab}_cc1', f'{ab}_cc2'])
            except Exception:
                pass
        else:
            for ab in MIC_ANTIBIOTICS:
                empty.update([ab, f'{ab}_cc1', f'{ab}_cc2'])

        if not selected_table_1:
            for ab in MIC_ANTIBIOTICS:
                empty.add(f'{ab}_cc1')
        if not selected_table_2:
            for ab in MIC_ANTIBIOTICS:
                empty.add(f'{ab}_cc2')

        return empty

    def post(self, request, *args, **kwargs):
        self.update_parameters(request)
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        return render(request, 'resultados.html', context=context)

    def update_parameters(self, request, *args, **kwargs):
        parameters = request.POST.copy()
        parameters_used = {}  # always start empty
        verbose_used = {}  # always start empty

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

        qs = qs.filter().order_by("isolate_name").select_related('sequenceanalysis')

        return qs

def heatmap_all_view(request):
    """Printable page: full resistome heatmap for all filtered records."""
    selected_genes = [g for g in request.GET.getlist('genes') if g]
    loci_type = request.GET.get('loci_type', 'muts')
    if not selected_genes:
        return HttpResponse("No genes selected.", status=400)

    qs = MultiFilter(request.GET, queryset=MetadataGeneral.objects.all().select_related('sequenceanalysis')).qs
    sa_dict = {
        sa.isolate_id_id: sa
        for sa in SequenceAnalysis.objects.filter(isolate_id__in=qs.values_list('isolate_id', flat=True))
    }
    cat_map = {'WT': 0, 'Mutation': 1, 'Polymorphism': 2, 'Both': 3}
    isolates, z_data, text_data = [], [], []
    for obj in qs:
        sa = sa_dict.get(obj.isolate_id)
        if not sa:
            continue
        muts = sa.mutational_resistome_muts or {}
        pols = sa.mutational_resistome_pols or {}
        isolates.append(obj.isolate_name or str(obj.isolate_id))
        z_data.append([cat_map[_get_gene_category(g, muts, pols)] for g in selected_genes])
        text_data.append([f"Muts: {muts.get(g,'WT')}<br>Pols: {pols.get(g,'WT')}" for g in selected_genes])

    heatmap_json = json.dumps({'isolates': isolates, 'genes': selected_genes, 'z': z_data, 'text': text_data})
    return render(request, 'heatmap_print.html', {'heatmap_json': heatmap_json})

def pipelines(request):
    return render(request, 'pipelines.html')


def documentacion(request):
    return render(request, 'documentacion.html')


# @login_required
def cargadatos(request):
    return render(request, 'cargadatos.html')


def contacto(request):
    return render(request, 'contacto.html')
