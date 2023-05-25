from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash


class EtapaAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Etapa(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    LOCAL = (
        ('STAR PADEL', 'Star Padel'),
    ) 
    
    GRUPO = (
        ('A', 'A'),
        ('B', 'B' ),
    )
    grupo = models.CharField('Turma Longeva', max_length=5, choices=GRUPO, null=True, blank=False)
    data = models.DateField('Data da etapa *', help_text='Use dd/mm/aaaa')
    local = models.CharField('Local da etapa *', max_length=15, choices=LOCAL, default='STAR PADEL', help_text='* Campos obrigatórios')
    total_duplas = models.IntegerField('Total de duplas', null=True, blank=True, default=0)
    total_chaves = models.IntegerField('Total de chaves', null=True, blank=True, default=0)    
    inscritos_direita = models.IntegerField('Total de direitas inscritos', null=True, blank=True, default=0)
    inscritos_esquerda = models.IntegerField('Total de esquerdas inscritos', null=True, blank=True, default=0)
    is_active = models.BooleanField(_('Ativo'), default=True, help_text='Se ativo, o curso pode ser usado no sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    etapas_ativas = EtapaAtivoManager()

    
    class Meta:
        ordering            =   ['grupo','-data']
        verbose_name        =   ('etapa')
        verbose_name_plural =   ('etapas')

    def __str__(self):
        return '%s: %s' % (self.grupo, self.data)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()        
        super(Etapa, self).save(*args, **kwargs)

    @property
    def vagas_esquerda(self):
        return self.total_duplas - self.inscritos_esquerda
    
    @property
    def vagas_direita(self):
        return self.total_duplas - self.inscritos_direita

    @property
    def get_absolute_url(self):
        return reverse('etapa_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('etapa_delete', args=[str(self.id)])
