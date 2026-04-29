from django.db import models

class Emprestimo(models.Model):
    dataRetirada = models.DateTimeField('Data de Retirada', help_text='Data da retirada')
    dataDevolucao = models.DateTimeField('Data de Devolução', help_text='Data da devolução')


    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'

    def __str__(self):
        return {self.dataRetirada}

class ReservaEmprestimo(models.Model):
    emprestimo = models.ForeignKey(Emprestimo, related_name='reservas',on_delete=models.CASCADE, null=True, blank=True)
    reserva = models.ForeignKey('reservas.Reserva', verbose_name='Reserva', related_name='reservas_emprestimo_emprestimo' ,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Reserva concluída'
        verbose_name_plural = 'Reservas concluídas'

    def __str__(self):
        return  str(self.reserva)