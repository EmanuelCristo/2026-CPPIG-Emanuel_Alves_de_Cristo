from django.db import models
from django.db.models import Max
from stdimage import StdImageField

import salas.models

STATUS_CHAVE = (
    ('D', 'Disponível'),
    ('Q', 'Quebrada'),
)

class Chave(models.Model):
    sala = models.OneToOneField(salas.models.Sala, verbose_name='Sala', unique=True, on_delete=models.CASCADE)
    quantidadeCopias = models.PositiveIntegerField(verbose_name='Quantidade de Cópias', default=1, help_text='Quantidade de cópias da chave')

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def save(self, *args, **kwargs):
        if self.pk is None:
            quantidade_anterior = 0
        else:
            quantidade_anterior = Chave.objects.get(pk=self.pk).quantidadeCopias

        super().save(*args, **kwargs)

        copias_a_criar = self.quantidadeCopias - quantidade_anterior

        if copias_a_criar > 0:
            numeros_existentes = list(
                CopiaChave.objects.filter(chave=self).values_list('numeroCopia', flat=True)
            )
            for _ in range(copias_a_criar):
                proximo_numero = 1

                while proximo_numero in numeros_existentes:
                    proximo_numero += 1

                CopiaChave.objects.create(
                    chave=self,
                    numeroCopia=proximo_numero,
                    status='D',
                )

                numeros_existentes.append(proximo_numero)

    def __str__(self):
        return f"{self.sala}"

class CopiaChave(models.Model):
    chave = models.ForeignKey(Chave, verbose_name='Chave', on_delete=models.CASCADE)
    numeroCopia = models.PositiveIntegerField(verbose_name='Numero da Cópia', default=1)
    status = models.CharField('Status', choices=STATUS_CHAVE, default='D', max_length=100, help_text='Status do chave')

    class Meta:
        verbose_name = 'Cópia da Chave'
        verbose_name_plural = 'Cópias das Chaves'
        unique_together = ('chave', 'numeroCopia')

    def delete(self, *args, **kwargs):
        chave_principal = self.chave

        super().delete(*args, **kwargs)

        if chave_principal.quantidadeCopias > 0:
            chave_principal.quantidadeCopias -= 1

            chave_principal.save(update_fields=['quantidadeCopias'])

    def __str__(self):
        return f"{self.chave.sala} - Cópia #{self.numeroCopia}"

