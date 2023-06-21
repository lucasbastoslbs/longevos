from django import forms
from django.db import models

from chave.models import Chave
from etapa.models import Etapa
from jogo.models import Jogo



class JogoForm(forms.ModelForm):
     

    class Meta:
        model = Jogo
        fields = ['fase', 'chave', 'timeA', 'timeB', 'placar_timeA_set1', 'placar_timeB_set1', 'placar_timeA_set2', 'placar_timeB_set2', 'placar_timeA_set3', 'placar_timeB_set3', 'vencedor']
    

