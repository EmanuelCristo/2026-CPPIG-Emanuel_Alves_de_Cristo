from django.urls import path

from porteiros.views import PorteiroListView, PorteiroAddView, PorteiroUpdateView, PorteiroDeleteView

urlpatterns = [
    path('porteiros', PorteiroListView.as_view(), name='porteiros'),
    path('porteiros/criar', PorteiroAddView.as_view(), name='porteiro_criar'),
    path('<int:pk>/porteiro/editar', PorteiroUpdateView.as_view(), name='porteiro_editar'),
    path('<int:pk>porteiro/deletar', PorteiroDeleteView.as_view(), name='porteiro_apagar'),
]