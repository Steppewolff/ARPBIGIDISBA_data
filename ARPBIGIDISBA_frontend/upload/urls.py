from django.urls import path
from . import views
# from .views import UploadListView # ResultadosTableView,

urlpatterns = [
    path('cargadatos', views.upload, name='cargadatos'),
    path('upload_summary', views.summary, name='upload_summary'),
    path('upload_modal', views.modal, name='upload_modal'),
    path('upload_confirm', views.confirm, name='upload_confirm'),
    path('descargar_manual_bdd/', views.descargar_manual_bdd, name='descargar_manual_bdd'),
    path('fk_save', views.fk_save, name='fk_save'),
]