from django.urls import path, include
from .views import hello_world, create_table, calcule_tukey, whats_tukey_test

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('create_table/', create_table, name='create_table'),
    path('calcule_tukey/', calcule_tukey, name='calcule_tukey'),
    path('o-que-e-teste-de-tukey/', whats_tukey_test, name='whats_tukey_test'),
]
