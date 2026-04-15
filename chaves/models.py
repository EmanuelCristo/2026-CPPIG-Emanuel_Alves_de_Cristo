from django.db import models
from stdimage import StdImageField


import salas.models


class Chave(models.Model):
    sala = models.OneToOneField(salas.models.Sala, verbose_name='Sala', on_delete=models.CASCADE)
  #  sala = models.CharField('Sala', max_length=100, help_text='Sala que a chave pertence')
  #  foto = StdImageField('Foto', upload_to='alunos', delete_orphans=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return self.nome

class CopiaChave(models.Model):
    chave = models.ForeignKey(Chave, verbose_name='Chave', on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=100, help_text='Status do chave')
