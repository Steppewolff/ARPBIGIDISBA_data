from django.urls import path
from . import views
# from .views import UploadListView # ResultadosTableView,

urlpatterns = [
    path('aplicaciones', views.applications, name='aplicaciones'),
]