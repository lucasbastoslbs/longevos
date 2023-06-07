from django import forms
from django.db import models

from chave.models import Chave
from etapa.models import Etapa


class ChaveForm(forms.ModelForm):
    etapa = forms.ModelChoiceField(label='Etapa ativa', queryset=Etapa.etapas_ativas.all())    

    class Meta:
        model = Chave
        fields = ['etapa', 'nome']
    