from django.urls import path
from . import views
from .views import DashboardListView # ResultadosTableView,

urlpatterns = [
    path('dashboard', DashboardListView.as_view(), name='dashboard'),
]