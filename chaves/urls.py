from django.urls import path

from chaves.views import ChavesView, ChaveAddView, ChaveUpdateView, ChaveDeleteView

urlpatterns = [
    path('chaves', ChavesView.as_view(), name='chaves'),
    path('chave/criar', ChaveAddView.as_view(), name='chave_criar'),
    path('<int:pk>/chave/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/chave/deletar/', ChaveDeleteView.as_view(), name='chave_apagar'),
]