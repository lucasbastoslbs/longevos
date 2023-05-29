from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash

class InscricaoAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InscricaoDireitaSemDuplaAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(com_dupla=False, posicao_etapa='DIREITA')
    

class InscricaoEsquerdaSemDuplaAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(com_dupla=False, posicao_etapa='ESQUERDA')


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
    com_dupla = models.BooleanField('Com dupla?', null=True, blank=True, default=False)
    
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    inscricoes_ativas = InscricaoAtivoManager()
    direitas_sem_dupla = InscricaoDireitaSemDuplaAtivoManager()
    esquerdas_sem_dupla = InscricaoEsquerdaSemDuplaAtivoManager()
    
    class Meta:
        ordering            =   ['etapa__grupo','-etapa__data', 'posicao_etapa', 'atleta__nome']
        verbose_name        =   ('inscrição')
        verbose_name_plural =   ('inscrições')
        unique_together     =   [['etapa','atleta']]

    def __str__(self):
        return "Etapa: %s. Atleta: %s. Posição na etapa: %s. Com dupla: %s" % (self.etapa, self.atleta, self.posicao_etapa, self.com_dupla)

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
    
    