from django.urls import path
from . import views
# from .views import UploadListView # ResultadosTableView,

urlpatterns = [
    path('cargadatos', views.upload, name='cargadatos'),
]