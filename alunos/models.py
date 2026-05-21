from django.db import models

from django.shortcuts import render
from stdimage import StdImageField

from servidores.models import Pessoa

class Aluno(Pessoa):
    matricula = models.CharField('Matrícula', max_length=15, unique=True, help_text='Matrícula do aluno')
    foto = StdImageField('Foto', upload_to='alunos', delete_orphans=True, null=True, blank=False)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        return super().nome