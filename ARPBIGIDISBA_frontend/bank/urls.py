from django.urls import path
from . import views

urlpatterns = [
    path('strain_bank/', views.freezer_view, name='strain_bank'),
    path('sample/<int:pk>/update/', views.sample_update_view, name='sample_update'),
    path('sample/<int:pk>/delete/', views.sample_delete_view, name='sample_delete'),
]