from django.urls import path

from emprestimos.views import EmprestimosListView, EmprestimoAddView, EmprestimoUpdateView, EmprestimoDeleteView, \
    EmprestimoFinalizarUpdateView, EmprestimosFinalizadosListView

urlpatterns = [
    path('emprestimos', EmprestimosListView.as_view(), name='emprestimos'),
    path('emprestimos/finalizados', EmprestimosFinalizadosListView.as_view(), name='emprestimos_finalizados'),
    path('emprestimo/criar', EmprestimoAddView.as_view(), name='emprestimo_criar'),
    path('<int:pk>/emprestimo/editar/', EmprestimoUpdateView.as_view(), name='emprestimo_editar'),
    path('<int:pk>/emprestimo/apagar/', EmprestimoDeleteView.as_view(), name='emprestimo_apagar'),
    path('<int:pk>/emprestimo/finalizar/', EmprestimoFinalizarUpdateView.as_view() , name='emprestimo_finalizar'),
]