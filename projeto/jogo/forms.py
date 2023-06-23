from django import forms
from django.db import models

from chave.models import ChaveDupla
from etapa.models import Etapa
from jogo.models import Jogo


class JogoCreateForm(forms.ModelForm):
    etapa = forms.ModelChoiceField(label='Etapa', queryset=Etapa.etapas_ativas.all())
    class Meta:
        model = Jogo
        fields = ['etapa', 'fase', 'chave', 'timeA', 'timeB']

class JogoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JogoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['etapa'].disabled = True
        self.fields['fase'].disabled = True
        self.fields['chave'].disabled = True
        self.fields['timeA'].disabled = True
        self.fields['timeB'].disabled = True
        idA = self.fields['timeA'].get_bound_field(form=self,field_name='timeA').value()
        idB = self.fields['timeB'].get_bound_field(form=self,field_name='timeB').value()
        self.fields['vencedor'] = forms.ModelChoiceField(label='Vencedor', queryset=ChaveDupla.objects.filter(id__in=[idA,idB]))


    class Meta:
        model = Jogo
        fields = ['etapa', 'fase', 'chave', 'timeA', 'timeB', 'placar_timeA_set1', 'placar_timeB_set1', 'placar_timeA_set2', 'placar_timeB_set2', 'placar_timeA_set3', 'placar_timeB_set3', 'vencedor']
    

class BuscaJogoForm(forms.Form):    
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    FASE = (
        (None,'-------------'),
        ('CLASSIFICATÓRIA', 'Classificatória'),
        ('DEZESSEIS', 'Dezesseis' ),
        ('DÉCIMA', 'Décima' ),
        ('OITAVAS', 'Oitavas' ),
        ('QUARTAS', 'Quartas' ),
        ('SEMI', 'Semi' ),
        ('FINAL', 'Final' ),
    )  
    etapa = forms.ModelChoiceField(label='Etapa', queryset=Etapa.etapas_ativas.all(), required=False)
    fase = forms.ChoiceField(label='Selecione a fase', choices=FASE, required=False)
    atleta = forms.CharField(label='Digite dados do atleta', required=False)
    
