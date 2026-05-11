import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django.db.models import Field, JSONField
from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap4Responsive, ColumnShiftTableBootstrap4, ColumnShiftTable, ColumnShiftTableBootstrap5Responsive

from .models import Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, FilePath

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
                return 'NO_SA'
            field = 'mutational_resistome_muts' if self.loci_type == 'muts' else 'mutational_resistome_pols'
            json_data = getattr(sa, field, None) or getattr(sa, 'mutational_resistome_muts', None)
            if json_data is None:
                return 'NO_JSON'
            val = json_data.get(self.gene_name)
            return val if val is not None else 'KEY_NOT_FOUND'
        except Exception as e:
            return f'ERR:{e}'

# def create_dynamic_table(*models, extra_columns=None):
#     attrs = {}
#     for model in models:
#         for field in model._meta.get_fields():
#             if isinstance(field, Field):
#                 if isinstance(field, JSONField):          # ← excluir JSON fields
#                     continue
#                 if model._meta.model_name == 'metadatageneral':
#                     accessor = f'{field.name}'
#                     column_name = f'{field.name}'
#                     attrs[column_name] = tables.Column(accessor=accessor)
#                 else:
#                     if '_id' in field.name:
#                         pass
#                     else:
#                         accessor = f'{model._meta.model_name}.{field.name}'
#                         column_name = f'{model._meta.model_name}_{field.name}'
#                         attrs[column_name] = tables.Column(accessor=accessor)
#
#         attrs['Meta'] = type('Meta', (), {
#             'template_name': 'django_tables2/bootstrap4.html',
#             'exclude': ('clinic_id', 'isolate_id',),
#             'export_formats': ["csv", "xlsx", "txt"],
#             'attrs': {'class': 'table table-dark table-striped table-hover table-responsive results'}
#         })
#     if extra_columns:
#         attrs.update(extra_columns)
#     return type('CombinedTable', (ColumnShiftTableBootstrap4, ColumnShiftTable, tables.Table), attrs)


def create_dynamic_table(*models, extra_columns=None):
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

    # Construir sequence con genes después de project_name
    gene_col_names = list(extra_columns.keys()) if extra_columns else []
    if extra_columns:
        attrs.update(extra_columns)

    if gene_col_names and 'project_name' in all_column_names:
        idx = all_column_names.index('project_name') + 1
        sequence = all_column_names[:idx] + gene_col_names + all_column_names[idx:]
    else:
        sequence = all_column_names + gene_col_names

    attrs['Meta'] = type('Meta', (), {
        'template_name': 'django_tables2/bootstrap4.html',
        'exclude': ('clinic_id', 'isolate_id',),
        'sequence': tuple(sequence),
        'export_formats': ["csv", "xlsx", "txt"],
        'attrs': {'class': 'table table-dark table-striped table-hover table-responsive results'}
    })

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


def create_mic_table(label1="BP Version 1", label2="BP Version 2"):
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
