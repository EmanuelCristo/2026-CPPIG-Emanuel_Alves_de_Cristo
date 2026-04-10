from django.urls import path

from servidores.views import ServidoresView, ServidorAddView, ServidorUpdateView, ServidorDeleteView

urlpatterns = [
    path('servidores', ServidoresView.as_view(), name='servidores'),
    path('servidor/criar', ServidorAddView.as_view(), name='servidor_criar'),
    path('<int:pk>/servidor/editar/', ServidorUpdateView.as_view(), name='servidor_editar'),
    path('<int:pk>/servidor/deletar/', ServidorDeleteView.as_view(), name='servidor_apagar'),
]