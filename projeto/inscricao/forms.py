from django import forms
from django.db import models

from usuario.models import Usuario

from .models import Inscricao
from etapa.models import Etapa


class InscricaoForm(forms.ModelForm):
    etapa = forms.ModelChoiceField(label='Etapa', queryset=Etapa.etapas_ativas.all())
    atleta = forms.ModelChoiceField(label='Atleta', queryset=Usuario.atletas.all())

    class Meta:
        model = Inscricao
        fields = ['etapa', 'atleta', 'posicao_etapa']
    


