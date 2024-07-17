import django_tables2 as tables
from django.db.models import Field

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
                    accessor = f'{model._meta.model_name}.{field.name}'
                    column_name = f'{model._meta.model_name}_{field.name}'
                    attrs[column_name] = tables.Column(accessor=accessor)

                pass

            attrs['Meta'] = type('Meta', (), {'template_name': 'django_tables2/bootstrap5.html', 'attrs': {
                'class': 'table table-dark table-striped table-hover table-responsive results'}})

            pass

    return type('CombinedTable', (tables.Table,), attrs)


CombinedTable = create_dynamic_table(MetadataGeneral, MetadataClinic, Mic, PhenotypicData, SequenceAnalysis, FilePath)


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
