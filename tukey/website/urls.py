from django.urls import path, include
from .views import hello_world, create_table, calcule_average

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('create_table/', create_table, name='create_table'),
    path('calcule_average/', calcule_average, name='calcule_average'),
]
