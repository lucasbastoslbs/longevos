from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash


class Dupla(models.Model):
    
    atleta_direita = models.ForeignKey('inscricao.Inscricao', verbose_name= 'Direita *', on_delete=models.PROTECT, related_name='atleta_direita')
    atleta_esquerda = models.ForeignKey('inscricao.Inscricao', verbose_name= 'Esquerda *', on_delete=models.PROTECT, related_name='atleta_esquerda')
    pontuacao_dupla = models.IntegerField('Pontuação somada atletas', null=True, blank=True)
    
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()

    
    class Meta:
        ordering            =   ['atleta_direita__etapa','-pontuacao_dupla']
        verbose_name        =   'dupla'
        verbose_name_plural =   'duplas'

    def __str__(self):
        return 'Direita: %s. Esquerda: %s' % (self.atleta_direita, self.atleta_esquerda)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.pontuacao_dupla = self.atleta_direita.atleta.pontuacao + self.atleta_esquerda.atleta.pontuacao
        self.atleta_direita.com_dupla = True
        self.atleta_esquerda.com_dupla = True
        self.atleta_direita.save()
        self.atleta_esquerda.save()
        self.pontuacao_dupla = self.atleta_direita.atleta.pontuacao + self.atleta_esquerda.atleta.pontuacao
        super(Dupla, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('dupla_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('dupla_delete', args=[str(self.id)])
