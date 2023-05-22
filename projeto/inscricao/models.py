from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Inscricao(models.Model): 
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    POSICAO = (
        ('DIREITA', 'Direita'),
        ('ESQUERDA', 'Esquerda' ),
    )
    
    etapa = models.ForeignKey('etapa.Etapa', verbose_name= 'Etapa da inscrição', on_delete=models.PROTECT, related_name='etapa')
    atleta = models.ForeignKey('usuario.Usuario', verbose_name= 'Atleta *', on_delete=models.PROTECT, related_name='atleta')

    posicao_etapa = models.CharField('Posição na quadra para esta etapa *', max_length=8, choices=POSICAO)
    
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['-etapa__data', 'atleta__nome']
        verbose_name        =   ('inscrição')
        verbose_name_plural =   ('inscrições')
        unique_together     =   [['etapa','atleta']]

    def __str__(self):
        return "Etapa: %s. Atleta: %s. Posição: %s." % (self.etapa, self.atleta, self.posicao)

    def save(self, *args, **kwargs):                
        if not self.slug:
            self.slug = gerar_hash()
        super(Inscricao, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('inscricao_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('inscricao_delete', args=[str(self.id)]) 
    
    