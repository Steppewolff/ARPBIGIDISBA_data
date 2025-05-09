from django.urls import path
from .views import freezer_view
from . import views

urlpatterns = [
    # path('', freezer_view, name='freezer'),
    path('strain_bank', views.freezer_view, name='strain_bank'),
]