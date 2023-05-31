from django.db import models


class Chave(models.Model):
    nome = models.CharField('Nome', max_length=1)
    etapa = models.ForeignKey('etapa.Etapa', on_delete=models.PROTECT)

    class Meta:
        ordering = ['nome']
        unique_together = [['nome', 'etapa']]


class ChaveDupla(models.Model):
    chave = models.ForeignKey('chave.Chave', on_delete=models.PROTECT)
    dupla = models.ForeignKey('dupla.Dupla', on_delete=models.PROTECT)