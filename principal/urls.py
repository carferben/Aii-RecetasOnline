from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path("load_data/", views.cargar_datos),
    path('loadRS/', views.loadRS),
    path("show_all/", views.show_all),
    path('show_all/<int:id_receta>/', views.mostrar_receta, name='mostrar_receta'),
]
