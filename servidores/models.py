from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome Completo')
    email = models.EmailField('Email', max_length=100, help_text='Endereço de e-mail')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

class Servidor(Pessoa):
    siape = models.CharField('Siape', max_length=7, help_text='Siape do servidor', unique=True)
    funcao = models.CharField('Função', max_length= 100, help_text='Função do Servidor')
    foto = StdImageField('Foto', upload_to='servidores', delete_orphans=True, null=True, blank=False)

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'
        ordering = [Upper('nome')]

    def __str__(self):
        return super().nome