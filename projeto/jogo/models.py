from django.db import models
from django.urls import reverse

from dupla.models import Dupla
from chave.models import ChaveDupla

from utils.gerador_hash import gerar_hash

class Jogo(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    FASE = (
        ('CLASSIFICATÓRIA', 'Classificatória'),
        ('DEZESSEIS', 'Dezesseis' ),
        ('DÉCIMA', 'Décima' ),
        ('OITAVAS', 'Oitavas' ),
        ('QUARTAS', 'Quartas' ),
        ('SEMI', 'Semi' ),
        ('FINAL', 'Final' ),
    )    
    
    fase = models.CharField('Fase da etapa *', max_length=15, choices=FASE,  help_text='* Campos obrigatórios')
    chave = models.ForeignKey('chave.Chave', null=True, blank=True, on_delete=models.PROTECT)
    etapa = models.ForeignKey('etapa.Etapa', null=True, blank=False, on_delete=models.PROTECT)
    timeA = models.ForeignKey('chave.ChaveDupla',  on_delete=models.PROTECT, related_name='timeA_chave_dupla')
    timeB = models.ForeignKey('chave.ChaveDupla', on_delete=models.PROTECT, related_name='timeB_chave_dupla')

    placar_timeA_set1 = models.DecimalField('Games vencidos Time A (1o set)',max_digits=2, decimal_places=0, null=True, blank=True, default= 0)
    placar_timeB_set1 = models.DecimalField('Games vencidos Time B (1o set)',max_digits=2, decimal_places=0, null=True, blank=True, default= 0)
    
    placar_timeA_set2 = models.DecimalField('Games vencidos Time A (2o set)',max_digits=2, decimal_places=0, null=True, blank=True, default= 0, help_text='Caso tenha ocorrido o set')
    placar_timeB_set2 = models.DecimalField('Games vencidos Time B (2o set)',max_digits=2, decimal_places=0, null=True, blank=True, default= 0, help_text='Caso tenha ocorrido o set')
    
    placar_timeA_set3 = models.DecimalField('Games vencidos Time A (3o set)',max_digits=2, decimal_places=0, null=True, default= 0, blank=True, help_text='Caso tenha ocorrido o set')
    placar_timeB_set3 = models.DecimalField('Games vencidos Time B (3o set)',max_digits=2, decimal_places=0, null=True, default= 0, blank=True, help_text='Caso tenha ocorrido o set')
    
    vencedor = models.ForeignKey('chave.ChaveDupla', on_delete=models.PROTECT, null=True, blank=True, related_name='vencedor')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering = ['fase','chave']
        unique_together     =   [['fase', 'timeA', 'timeB']]
        verbose_name        =   ('jogo')
        verbose_name_plural =   ('jogos')

    def __str__(self):
        return "Fase: %s. TimeA: %s versus TimeB: %s." % (self.fase, self.timeA, self.timeB)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash() 
        super(Jogo, self).save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('jogo_update', args=[str(self.id)])
    
    @property
    def get_delete_url(self):
        return reverse('jogo_delete', args=[str(self.id)])