from django.db import models

class Chaves(models.Model):
    nome = models.CharField(max_length=100)