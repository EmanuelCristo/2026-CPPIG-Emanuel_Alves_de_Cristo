from django.urls import path

from .views import SalasView, SalaAddView

urlpatterns = [
    path('salas', SalasView.as_view(), name='salas'),
    path('sala/criar', SalaAddView.as_view(), name='sala_criar'),
]