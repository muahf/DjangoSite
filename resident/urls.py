from django.urls import path
from . import views

app_name = 'resident'

urlpatterns = [
    path('', views.home, name='home'),

    # Pathogens
    path('pathogens/', views.pathogen_list, name='pathogen'),
    path('pathogens/add/', views.pathogen_create, name='pathogen_create'),
    path('pathogens/<int:pk>/', views.pathogen_detail, name='pathogen_detail'),
    path('pathogens/<int:pk>/edit/', views.pathogen_update, name='pathogen_update'),
    path('pathogens/<int:pk>/delete/', views.pathogen_delete, name='pathogen_delete'),

    # Researchers
    path('researchers/', views.researcher_list, name='researcher'),
    path('researchers/add/', views.researcher_create, name='researcher_create'),
    path('researchers/<int:pk>/', views.researcher_detail, name='researcher_detail'),
    path('researchers/<int:pk>/edit/', views.researcher_update, name='researcher_update'),
    path('researchers/<int:pk>/delete/', views.researcher_delete, name='researcher_delete'),
]