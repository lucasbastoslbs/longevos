from django import forms
from django.db import models

from dupla.models import Dupla
from etapa.models import Etapa
from inscricao.models import Inscricao



class DuplaForm(forms.ModelForm):
    atleta_direita = forms.ModelChoiceField(label='Direita', queryset=Inscricao.direitas_sem_dupla.all())
    atleta_esquerda = forms.ModelChoiceField(label='Esquerda', queryset=Inscricao.esquerdas_sem_dupla.all())

    class Meta:
        model = Dupla
        fields = ['atleta_direita', 'atleta_esquerda','pontuacao_dupla']
    

class BuscaDuplaForm(forms.Form):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    POSICAO = (
        (None,'-------------'),
        ('DIREITA', 'Direita'),
        ('ESQUERDA', 'Esquerda' ),
        ('AMBAS', 'Ambas' ),
    )
    atleta = forms.CharField(label='Digite dados do atleta', required=False)
    etapa = forms.ModelChoiceField(label='Etapa', queryset=Etapa.etapas_ativas.all(), required=False)
    # posicao = forms.ChoiceField(label='Selecione a posição do atleta', choices=POSICAO, required=False)
