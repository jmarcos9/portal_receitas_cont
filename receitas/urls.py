from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:receita_id>receita', views.receita, name='receita')
]