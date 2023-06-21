from django import forms
from django.db import models

from chave.models import Chave
from etapa.models import Etapa
from jogo.models import Jogo


class JogoForm(forms.ModelForm):
     

    class Meta:
        model = Jogo
        fields = ['fase', 'chave', 'timeA', 'timeB', 'placar_timeA_set1', 'placar_timeB_set1', 'placar_timeA_set2', 'placar_timeB_set2', 'placar_timeA_set3', 'placar_timeB_set3', 'vencedor']
    

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
    
