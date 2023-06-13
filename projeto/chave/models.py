from django.db import models
from django.urls import reverse


class Chave(models.Model):
    nome = models.CharField('Nome', max_length=1, help_text="A ou B ou C ou D ou ...")
    etapa = models.ForeignKey('etapa.Etapa', on_delete=models.PROTECT)

    class Meta:
        ordering = ['nome']
        unique_together = [['nome', 'etapa']]
    
    
    def __str__(self):
        return '%s' % (self.nome)

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super(Chave, self).save(*args, **kwargs)
        
    @property
    def lista_duplas_chave(self):
        lista = ChaveDupla.objects.filter(chave=self)
        return lista
    
    @property
    def get_delete_url(self):
        return reverse('chave_delete', args=[str(self.id)])

class ChaveDupla(models.Model):
    chave = models.ForeignKey('chave.Chave', on_delete=models.PROTECT)
    dupla = models.ForeignKey('dupla.Dupla', on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['chave']      
        unique_together = [['dupla']]
    

    def save(self, *args, **kwargs):
        super(ChaveDupla, self).save(*args, **kwargs)
        
    @property
    def get_dupla_em_chave_delete_url(self):
        return reverse('chavedupla_delete', args=[str(self.id)])
