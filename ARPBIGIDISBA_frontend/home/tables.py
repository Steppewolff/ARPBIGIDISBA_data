import django_tables2 as tables
from .models import Mic, Fenotipo, Secuencia, MetadataGeneral

class MicTable(tables.Table):
    class Meta:
        model = Mic
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('aislado', 'fep', 'cip', 'imi', 'col', 'atm', 'caz_cloxa', 'imi_cloxa',)
        attrs = {'class': 'table table-dark table-striped table-hover table-responsive'}

class FenotipoTable(tables.Table):
    class Meta:
        model = Fenotipo
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('fenotipo_id', 'test_cloxa', 'test_mbl', 'test_blee',)
        attrs = {'class': 'table table-dark table-striped table-hover table-responsive'}

class SecuenciaTable(tables.Table):
    class Meta:
        model = Secuencia
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('secuencia_id', 'clon', 'complejo_clonal', 'serotipo_insilico',)
        attrs = {'class': 'table table-dark table-sm table-hover'}
