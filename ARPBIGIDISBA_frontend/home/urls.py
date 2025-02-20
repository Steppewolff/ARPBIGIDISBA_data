from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import ResultadosListView # ResultadosTableView,

urlpatterns = [
    path('', views.home, name='home'),
    path('busqueda', views.busqueda, name='busqueda'),
    path('resultados', ResultadosListView.as_view(), name='resultados'),
    path('pipelines', views.pipelines, name='pipelines'),
    path('documentacion', views.documentacion, name='documentacion'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    # path('contacto', views.contacto, name='contacto'),
    # path('aplicaciones', views.aplicaciones, name='aplicaciones'),
]