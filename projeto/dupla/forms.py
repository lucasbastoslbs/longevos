from django import forms
from django.db import models

from dupla.models import Dupla
from inscricao.models import Inscricao


class DuplaForm(forms.ModelForm):
    atleta_direita = forms.ModelChoiceField(label='Direita', queryset=Inscricao.direitas_sem_dupla.all())
    atleta_esquerda = forms.ModelChoiceField(label='Esquerda', queryset=Inscricao.esquerdas_sem_dupla.all())

    class Meta:
        model = Dupla
        fields = ['atleta_direita', 'atleta_esquerda','pontuacao_dupla']
    


