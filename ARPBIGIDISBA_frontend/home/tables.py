import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django.db.models import Field
from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap4Responsive, ColumnShiftTable, ColumnShiftTableBootstrap5Responsive

from .models import Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, FilePath

def create_dynamic_table(*models):
    attrs = {}

    for model in models:
        for field in model._meta.get_fields():
            if isinstance(field, Field):
                # attrs[f'_{field.name}'] = tables.Column(accessor=f'{str(model)}.{field.name}')
                if model._meta.model_name == 'metadatageneral':
                    accessor = f'{field.name}'
                    column_name = f'{field.name}'
                    attrs[column_name] = tables.Column(accessor=accessor)
                else:
                    if '_id' in field.name:
                        pass
                    else:
                        accessor = f'{model._meta.model_name}.{field.name}'
                        column_name = f'{model._meta.model_name}_{field.name}'
                        attrs[column_name] = tables.Column(accessor=accessor)

                pass

            attrs['Meta'] = type('Meta', (), {'template_name': 'django_tables2/bootstrap5.html', 'exclude' : ('clinic_id', 'isolate_id',), 'export_formats' : '["csv", "xlsx", "txt"]', 'attrs': {
                'class': 'table table-dark table-striped table-hover table-responsive results'}})

            pass

    return type('CombinedTable', (ColumnShiftTableBootstrap4Responsive, ExportMixin, ColumnShiftTable, tables.Table), attrs)


CombinedTable = create_dynamic_table(MetadataGeneral, MetadataClinic, Mic, PhenotypicData, SequenceAnalysis, FilePath)

class MicTable(tables.Table):
    isolate_name = tables.Column(accessor='isolate_id.isolate_name')

    class Meta:
        model = Mic
        fields = ("isolate_name", "pip", "pip_clinical_category", "pip_tz", "pip_tz_clinical_category", "fep", "fep_clinical_category", "cfdc", "cfdc_clinical_category", "caz", "caz_clinical_category", "caz_avi", "caz_avi_clinical_category", "ctz", "ctz_clinical_category", "imi", "imi_clinical_category", "imi_rel", "imi_rel_clinical_category", "mer", "mer_clinical_category", "mer_vab", "mer_vab_clinical_category", "azt", "azt_clinical_category", "azt_avi", "azt_avi_clinical_category", "cip", "cip_clinical_category", "dlx", "dlx_clinical_category", "lvx", "lvx_clinical_category", "mxl", "mxl_clinical_category", "ami", "ami_clinical_category", "gen", "gen_clinical_category", "net", "net_clinical_category", "tob", "tob_clinical_category", "col", "col_clinical_category", "fo", "fo_clinical_category", "tic", "tic_clinical_category", "ptz", "ptz_clinical_category", "taz", "taz_clinical_category", "cza", "cza_clinical_category", "tol", "tol_clinical_category", "atm", "atm_clinical_category")
        attrs = {'class': 'table table-dark table-striped table-hover table-responsive'}


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
