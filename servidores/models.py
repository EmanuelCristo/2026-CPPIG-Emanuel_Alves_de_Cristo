from django.db import models
from stdimage import StdImageField


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome Completo')
    email = models.EmailField('Email', max_length=100, help_text='Endereço de e-mail')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

class Servidor(Pessoa):
    siape = models.CharField('Siape', max_length=50, help_text='Siape do servidor')
    funcao = models.CharField('Função', max_length= 100, help_text='Função do Servidor')
    foto = StdImageField('Foto', upload_to='servidores', delete_orphans=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'

    def __str__(self):
        return super().nome