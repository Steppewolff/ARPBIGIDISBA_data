from django.urls import path
from . import views
from .views import ResultadosListView # ResultadosTableView,

urlpatterns = [
    path('', views.home, name='home'),
    path('busqueda', views.busqueda, name='busqueda'),
    path('resultados', ResultadosListView.as_view(), name='resultados'),
    path('pipelines', views.pipelines, name='pipelines'),
    path('documentacion', views.documentacion, name='documentacion'),
    path('cargadatos', views.cargadatos, name='cargadatos'),
    path('contacto', views.contacto, name='contacto'),
]