from django.urls import path
from . import views
# from .views import UploadListView # ResultadosTableView,

urlpatterns = [
    path('aplicaciones', views.applications, name='aplicaciones'),
    path('amr_score_prediction', views.amr_score_prediction, name='amr_score_prediction'),
]