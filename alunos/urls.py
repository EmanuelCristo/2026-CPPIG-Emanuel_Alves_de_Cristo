from django.urls import path

from alunos.views import AlunosView, AlunoAddView, AlunoUpdateView, AlunoDeleteView

urlpatterns = [
    path('alunos', AlunosView.as_view(), name='alunos'),
    path('aluno/criar', AlunoAddView.as_view(), name='aluno_criar'),
    path('<int:pk>/aluno/editar/', AlunoUpdateView.as_view(), name='aluno_editar'),
    path('<int:pk>/aluno/deletar/', AlunoDeleteView.as_view(), name='aluno_apagar'),
]