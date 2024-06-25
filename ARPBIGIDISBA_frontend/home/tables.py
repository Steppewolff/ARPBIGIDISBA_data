import django_tables2 as tables
from .models import Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral


class MicTable(tables.Table):
    class Meta:
        model = Mic
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('isolate', 'fep', 'cip', 'imi', 'col', 'atm', 'caz_cloxa', 'imi_cloxa',)
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
