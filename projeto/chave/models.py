from django.db import models


class Chave(models.Model):
    nome = models.CharField('Nome', max_length=1)
    etapa = models.ForeignKey('etapa.Etapa', on_delete=models.PROTECT)

    class Meta:
        ordering = ['nome']
        unique_together = [['nome', 'etapa']]
    
    
    def __str__(self):
        return '%s' % (self.nome)

    def save(self, *args, **kwargs):
        super(Chave, self).save(*args, **kwargs)
        
    @property
    def lista_duplas_chave(self):
        lista = ChaveDupla.objects.filter(chave=self)
        return lista

class ChaveDupla(models.Model):
    chave = models.ForeignKey('chave.Chave', on_delete=models.PROTECT)
    dupla = models.ForeignKey('dupla.Dupla', on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['chave']      
    
    # def __str__(self):
    #     return 'Chave: %s: Dupla %s.' % (self.chave, self.dupla)

    def save(self, *args, **kwargs):
        super(ChaveDupla, self).save(*args, **kwargs)