from django.urls import path

from reservas.views import ReservasListView, ReservaAddView, ReservaUpdateView, ReservaDeleteView

urlpatterns = [
    path('reservas', ReservasListView.as_view(), name='reservas'),
    path('reserva/criar', ReservaAddView.as_view(), name='reserva_criar'),
    path('<int:pk>/reserva/editar/', ReservaUpdateView.as_view(), name='reserva_editar'),
    path('<int:pk>/reserva/deletar/', ReservaDeleteView.as_view(), name='reserva_apagar'),
]