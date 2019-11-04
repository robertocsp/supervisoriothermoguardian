from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:parametro_id>/', views.testaparametro, name='testaparametro'),
    path('retornoparametros/', views.retornoparametros, name='retornoparametros')
]