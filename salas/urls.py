from django.urls import path

from .views import SalasView, SalaAddView, SalaUpdateView, SalaDeleteView

urlpatterns = [
    path('salas', SalasView.as_view(), name='salas'),
    path('sala/criar', SalaAddView.as_view(), name='sala_criar'),
    path('<int:pk>/sala/editar/', SalaUpdateView.as_view(), name='sala_editar'),
    path('<int:pk>/sala/deletar/', SalaDeleteView.as_view(), name='sala_apagar'),
]