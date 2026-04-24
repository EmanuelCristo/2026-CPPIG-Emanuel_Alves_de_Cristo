from django.db import models

from chaves.models import Chave
from servidores.models import Pessoa, Servidor


class Reserva(models.Model):
    chave = models.ForeignKey(Chave, verbose_name='Chave', on_delete=models.CASCADE, help_text='Chave que deseja reservar')
    inicioReserva = models.DateField(verbose_name='Inicio da Reserva', help_text='Data de inicio da reserva')
    fimReserva = models.DateField(verbose_name='Fim da Reserva', help_text='Data de fim da reserva')
    titular = models.ForeignKey(Servidor, verbose_name='Titular' ,on_delete=models.CASCADE, help_text='Titular da reserva')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return self.chave