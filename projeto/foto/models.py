from __future__ import unicode_literals

import os

from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash

class FotoAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Foto(models.Model): 
    titulo = models.CharField('Título da foto', max_length=50, help_text="Uma pequena frase para aparecer na capa do sistema")
    arquivo = models.FileField('Arquivo .png', upload_to='midias', help_text='Use arquivo .png para enviar seu arquivo')
    data_publicacao = models.DateTimeField('Data e hora de atualização do registro', auto_now=True)
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    fotos_ativas = FotoAtivoManager()
    
    class Meta:
        ordering            =   ['data_publicacao','titulo']
        verbose_name        =   ('foto')
        verbose_name_plural =   ('fotos')

    def __str__(self):
        return "%s - %s" % (self.titulo, self.data_publicacao)

    def save(self, *args, **kwargs):                        
        if not self.slug:
            self.slug = gerar_hash()
        super(Foto, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('foto_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('foto_delete', args=[str(self.id)]) 
    
#triggers para limpeza dos arquivos apagados ou alterados. No Django é chamado de signals
#deleta o arquivo fisico ao excluir o item midia
@receiver(models.signals.post_delete, sender=Foto)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.arquivo:
        if os.path.isfile(instance.arquivo.path):
            os.remove(instance.arquivo.path)

#deleta o arquivo fisico ao alterar o arquivo do item midia
@receiver(models.signals.pre_save, sender=Foto)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        obj = Foto.objects.get(pk=instance.pk)

        if not obj.arquivo:
            return False

        old_file = obj.arquivo
    except Foto.DoesNotExist:
        return False

    new_file = instance.arquivo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
