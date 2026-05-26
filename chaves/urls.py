from django.urls import path

from chaves.views import ChavesListView, ChaveAddView, ChaveUpdateView, ChaveDeleteView, CopiasChaveListView, \
    CopiasChaveUpdateView, CopiasChaveDeleteView

urlpatterns = [
    path('chaves', ChavesListView.as_view(), name='chaves'),
    path('chave/criar', ChaveAddView.as_view(), name='chave_criar'),
    path('<int:pk>/chave/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/chave/deletar/', ChaveDeleteView.as_view(), name='chave_apagar'),
    path('<int:pk>/chave/copias', CopiasChaveListView.as_view(), name='chave_copias'),
    path('<int:pk>/copia/editar/', CopiasChaveUpdateView.as_view(), name='copia_editar'),
    path('<int:pk>/copia/deletar', CopiasChaveDeleteView.as_view(), name='copia_apagar'),
]