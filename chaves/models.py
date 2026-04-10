from django.db import models
from stdimage import StdImageField


class Chave(models.Model):
    sala = models.CharField('Sala', max_length=100, help_text='Sala que a chave pertence')
    quantidadeCopias = models.CharField('Quantidade de Cópias', max_length=5, help_text='Quantidade de cópias da chave')
  #  foto = StdImageField('Foto', upload_to='alunos', delete_orphans=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return self.nome