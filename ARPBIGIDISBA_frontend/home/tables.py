import django_tables2 as tables
import re
from django_tables2.export.views import ExportMixin
from django.db.models import Field, JSONField
from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap4Responsive, ColumnShiftTableBootstrap4, ColumnShiftTable, ColumnShiftTableBootstrap5Responsive

from .models import Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, FilePath

LOCUS_RE = re.compile(r'^(PA(?:LES|14)?\d{4,5})', re.IGNORECASE)

def _extract_locus(key):
    m = LOCUS_RE.match(key)
    return m.group(1) if m else key

class GeneColumn(tables.Column):
    """Column that reads a single gene value from a SequenceAnalysis JSON field."""
    def __init__(self, gene_name, loci_type='muts', **kwargs):
        self.gene_name = gene_name
        self.loci_type = loci_type
        kwargs.setdefault('verbose_name', gene_name)
        kwargs.setdefault('orderable', False)
        kwargs.setdefault('accessor', 'isolate_name')  # accessor válido que siempre resuelve
        super().__init__(**kwargs)

    def render(self, value, record):
        try:
            sa = getattr(record, 'sequenceanalysis', None)
            if sa is None:
                return ''
            field = 'mutational_resistome_muts' if self.loci_type == 'muts' else 'mutational_resistome_pols'
            json_data = getattr(sa, field, None) or getattr(sa, 'mutational_resistome_muts', None)
            if json_data is None:
                return ''
            # Exact match primero, luego por locus prefix
            if self.gene_name in json_data:
                val = json_data[self.gene_name]
            else:
                val = next((v for k, v in json_data.items() if _extract_locus(k) == self.gene_name), None)
            return val if val is not None else ''
        except Exception as e:
            return f'ERR:{e}'

# COLUMN ORDER: metadata > clinic > MIC > ecdc/dtr > typing > acquired > phenotypic > filepath > genes
_METADATA_GENERAL_COLS = [
    'isolate_name', 'isolate_project_code', 'species', 'project_name',
    'isolation_day', 'isolation_month', 'isolation_year', 'isolation_date',
    'isolate_source',
]
_METADATA_CLINIC_COLS = [
    'metadataclinic_patient_code', 'metadataclinic_sample_type',
    'metadataclinic_hospital', 'metadataclinic_collection_ward',
]

_MIC_COLS = [f'mic_{f}' for f in [
    'tic', 'tic_clinical_category',
    'pip', 'pip_clinical_category',
    'pip_tz', 'pip_tz_clinical_category',
    'caz', 'caz_clinical_category',
    'caz_avi', 'caz_avi_clinical_category',
    'tol', 'tol_clinical_category',
    'ctz', 'ctz_clinical_category',
    'fep', 'fep_clinical_category',
    'cfdc', 'cfdc_clinical_category',
    'fep_tan', 'fep_tan_clinical_category',
    'fep_zid', 'fep_zid_clinical_category',
    'fdc_xer', 'fdc_xer_clinical_category',
    'atm', 'atm_clinical_category',
    'azt_avi', 'azt_avi_clinical_category',
    'imi', 'imi_clinical_category',
    'imi_rel', 'imi_rel_clinical_category',
    'mer', 'mer_clinical_category',
    'mer_vab', 'mer_vab_clinical_category',
    'mer_nac', 'mer_nac_clinical_category',
    'mer_xer', 'mer_xer_clinical_category',
    'ami', 'ami_clinical_category',
    'tob', 'tob_clinical_category',
    'gen', 'gen_clinical_category',
    'net', 'net_clinical_category',
    'cip', 'cip_clinical_category',
    'lvx', 'lvx_clinical_category',
    'dlx', 'dlx_clinical_category',
    'mxl', 'mxl_clinical_category',
    'col', 'col_clinical_category',
    'fo', 'fo_clinical_category',
    'taz', 'taz_clinical_category',
    'avi', 'avi_clinical_category',
    'rel', 'rel_clinical_category',
    'nac', 'nac_clinical_category',
    'dur', 'dur_clinical_category',
    'xer', 'xer_clinical_category',
]]

# Fenotípico: resumen primero, resto después de resistencias adquiridas
_PHENOTYPIC_OVERVIEW_COLS = [
    'phenotypicdata_ecdc_resistance_profile',
    'phenotypicdata_dtr_profile',
]
_PHENOTYPIC_OTHER_COLS = [
    'phenotypicdata_cloxa_test', 'phenotypicdata_mbl_test', 'phenotypicdata_esbl_test',
    'phenotypicdata_class_a_carbapenemase_test',
    'phenotypicdata_invitro_serotype',
    'phenotypicdata_hypermutator_phenotype', 'phenotypicdata_morphotype',
    'phenotypicdata_virulence', 'phenotypicdata_cevs',
    'phenotypicdata_atb_susceptibility_method', 'phenotypicdata_atb_susceptibility_method_other',
    'phenotypicdata_broth_type', 'phenotypicdata_commercial_panel_name',
    'phenotypicdata_idsa_resistance_profile', 'phenotypicdata_phenotypic_comments',
]

# Secuencia: tipificación primero, resistencias adquiridas al final
_SEQUENCE_TYPING_COLS = [
    'sequenceanalysis_sequence_type', 'sequenceanalysis_clonal_complex',
    'sequenceanalysis_insilico_serotype',
    'sequenceanalysis_oprd_reference', 'sequenceanalysis_pdc_variant',
    'sequenceanalysis_piu_reference',
]
_SEQUENCE_ACQUIRED_COLS = [
    'sequenceanalysis_ame_loci', 'sequenceanalysis_beta_lactamase_loci',
    'sequenceanalysis_fluoroquinolones_loci', 'sequenceanalysis_other_acq_loci',
]

_FILEPATH_COLS = [
    'filepath_fastq_path', 'filepath_denovo_assembly_path',
    'filepath_denovo_assembly_ena_url', 'filepath_ena_accession',
]

# Orden final: metadata → MIC → ecdc/dtr → tipificación → resistencias adquiridas
#              → resto fenotípico → filepath  (genes se añaden dinámicamente)
_BASE_SEQUENCE = (
    _METADATA_GENERAL_COLS
    + _METADATA_CLINIC_COLS
    + _MIC_COLS
    + _PHENOTYPIC_OVERVIEW_COLS
    + _SEQUENCE_TYPING_COLS
    + _SEQUENCE_ACQUIRED_COLS
    + _PHENOTYPIC_OTHER_COLS
    + _FILEPATH_COLS
)

def create_dynamic_table(*models, extra_columns=None, empty_columns=None):
    attrs = {}
    all_column_names = []

    for model in models:
        for field in model._meta.get_fields():
            if isinstance(field, Field):
                if isinstance(field, JSONField):
                    continue
                if model._meta.model_name == 'metadatageneral':
                    column_name = f'{field.name}'
                    attrs[column_name] = tables.Column(accessor=f'{field.name}')
                    all_column_names.append(column_name)
                else:
                    if '_id' in field.name:
                        pass
                    else:
                        accessor = f'{model._meta.model_name}.{field.name}'
                        column_name = f'{model._meta.model_name}_{field.name}'
                        attrs[column_name] = tables.Column(accessor=accessor)
                        all_column_names.append(column_name)

    gene_col_names = list(extra_columns.keys()) if extra_columns else []
    if extra_columns:
        attrs.update(extra_columns)

    # Secuencia explícita; columnas no listadas van al final, genes al final del todo
    known = set(_BASE_SEQUENCE)
    all_attrs = set(all_column_names + gene_col_names)
    extra_generated = [c for c in all_column_names if c not in known]
    sequence = [c for c in _BASE_SEQUENCE if c in all_attrs] + extra_generated + gene_col_names

    attrs['Meta'] = type('Meta', (), {
        'template_name': 'django_tables2/bootstrap4.html',
        'exclude': ('clinic_id', 'isolate_id', 'isolate_comments'),
        'sequence': tuple(sequence),
        'export_formats': ["csv", "xlsx", "txt"],
        'attrs': {'class': 'table table-dark table-striped table-hover table-responsive results'}
    })

    _empty = frozenset(empty_columns or [])

    def get_column_default_show(self):
        return [c for c in self.sequence if c not in _empty]

    attrs['get_column_default_show'] = get_column_default_show

    return type('CombinedTable', (ColumnShiftTableBootstrap4, ColumnShiftTable, tables.Table), attrs)

CombinedTable = create_dynamic_table(MetadataGeneral, MetadataClinic, Mic, PhenotypicData, SequenceAnalysis, FilePath)

# Ordered list of antibiotic fields to show in the MIC table.
MIC_ANTIBIOTICS = ['tic',
          'pip',
          'pip_tz',
          'caz',
          'caz_avi',
          'tol',
          'ctz',
          'fep',
          'cfdc',
          'fep_tan',
          'fep_zid',
          'fdc_xer',
          'atm',
          'azt_avi',
          'imi',
          'imi_rel',
          'mer',
          'mer_vab',
          'mer_nac',
          'mer_xer',
          'ami',
          'tob',
          'gen',
          'net',
          'cip',
          'lvx',
          'dlx',
          'mxl',
          'col',
          'fo',
          'taz',
          'avi',
          'rel',
          'nac',
          'dur',
          'xer',
          ]

class MicTable(tables.Table):
    isolate_name = tables.Column(accessor='isolate_id.isolate_name')

    class Meta:
        model = Mic
        fields = ("isolate_name", "pip", "pip_clinical_category", "pip_tz", "pip_tz_clinical_category", "fep", "fep_clinical_category", "cfdc", "cfdc_clinical_category", "caz", "caz_clinical_category", "caz_avi", "caz_avi_clinical_category", "ctz", "ctz_clinical_category", "imi", "imi_clinical_category", "imi_rel", "imi_rel_clinical_category", "mer", "mer_clinical_category", "mer_vab", "mer_vab_clinical_category", "azt", "azt_clinical_category", "azt_avi", "azt_avi_clinical_category", "cip", "cip_clinical_category", "dlx", "dlx_clinical_category", "lvx", "lvx_clinical_category", "mxl", "mxl_clinical_category", "ami", "ami_clinical_category", "gen", "gen_clinical_category", "net", "net_clinical_category", "tob", "tob_clinical_category", "col", "col_clinical_category", "fo", "fo_clinical_category", "tic", "tic_clinical_category", "ptz", "ptz_clinical_category", "taz", "taz_clinical_category", "cza", "cza_clinical_category", "tol", "tol_clinical_category", "atm", "atm_clinical_category")
        attrs = {'class': 'table table-dark table-striped table-hover table-responsive results'}


def create_mic_table(label1="BP Version 1", label2="BP Version 2", empty_columns=None):
    """
    Returns a MicTable class with two computed clinical-category
    columns per antibiotic (cc1 and cc2), labelled with the names of the two
    breakpoint table versions selected by the user.

    """
    attrs = {
        'isolate_name': tables.Column(
            accessor='isolate_id.isolate_name',
            verbose_name='Isolate',
        ),
    }
    sequence = ['isolate_name']

    for ab in MIC_ANTIBIOTICS:
        col_cc1 = f'{ab}_cc1'
        col_cc2 = f'{ab}_cc2'

        # MIC value column (real model field)
        attrs[ab] = tables.Column(verbose_name=ab.upper())

        # Computed clinical-category columns (injected at runtime via setattr)
        attrs[col_cc1] = tables.Column(
            accessor=f'{ab}_clinical_category_1',
            verbose_name=label1,
            default='—',
        )
        attrs[col_cc2] = tables.Column(
            accessor=f'{ab}_clinical_category_2',
            verbose_name=label2,
            default='—',
        )

        sequence += [ab, col_cc1, col_cc2]

    attrs['Meta'] = type(
        'Meta', (), {
            'model': Mic,
            'sequence': tuple(sequence),
            'attrs': {'class': 'table table-dark table-striped table-hover table-responsive results'},
            'export_formats': ["csv", "xlsx", "txt"],
        })

    _empty = frozenset(empty_columns or [])
    def get_column_default_show(self):
        return [c for c in self.sequence if c not in _empty]
    attrs['get_column_default_show'] = get_column_default_show

    return type('DynamicMicTable', (ColumnShiftTableBootstrap4, tables.Table), attrs)

class MetadataGeneralTable(tables.Table):
    class Meta:
        model = MetadataGeneral
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('project_name', 'isolate_name', 'species', 'isolate_source', 'isolation_date', 'pip', 'pip_tz', 'fep')
        attrs = {'class': 'table table-dark table-striped table-hover table-responsive'}


class FenotipoTable(tables.Table):
    class Meta:
        model = PhenotypicData
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('isolate', 'cloxa_test', 'mbl_test', 'ecdc_resistance_profile',)
        attrs = {'class': 'table table-dark table-striped table-hover table-responsive'}


class SecuenciaTable(tables.Table):
    class Meta:
        model = SequenceAnalysis
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('isolate', 'sequence_type', 'clonal_complex', 'insilico_serotype',)
        attrs = {'class': 'table table-dark table-sm table-hover'}
