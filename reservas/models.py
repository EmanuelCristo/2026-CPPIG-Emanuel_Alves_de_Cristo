from django.db import models

import chaves.models
import servidores.models
from chaves.models import Chave
from servidores.models import Pessoa


class Reserva(models.Model):
    chave = models.ForeignKey(chaves.models.Chave, verbose_name='Chave', on_delete=models.CASCADE, help_text='Chave que deseja reservar')
    inicioReserva = models.DateField(verbose_name='Inicio da Reserva', help_text='Data de inicio da reserva')
    fimReserva = models.DateField(verbose_name='Fim da Reserva', help_text='Data de fin da reserva')
    Titular = models.ForeignKey(servidores.models.Pessoa, verbose_name='Titular' ,on_delete=models.CASCADE, help_text='Titular da reserva')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"{self.chave}"