from django.urls import path

from emprestimos.views import EmprestimosListView,  EmprestimoAddView, EmprestimoUpdateView

urlpatterns = [
    path('emprestimos', EmprestimosListView.as_view(), name='emprestimos'),
    path('emprestimo/criar', EmprestimoAddView.as_view(), name='emprestimo_criar'),
    path('<int:pk>/emprestimo/editar/', EmprestimoUpdateView.as_view(), name='emprestimo_editar'),
]