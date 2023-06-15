from django import forms
from django.db import models

from chave.models import Chave, ChaveDupla
from etapa.models import Etapa


class ChaveForm(forms.ModelForm):
    etapa = forms.ModelChoiceField(label='Etapa ativa', queryset=Etapa.etapas_ativas.all())    

    class Meta:
        model = Chave
        fields = ['etapa', 'nome']
    

class ChaveDuplaForm(forms.ModelForm):
    dupla = forms.ModelChoiceField(label='Dupla', queryset=ChaveDupla.duplas_sem_chave.all())    

    class Meta:
        model = ChaveDupla
        fields = ['chave', 'dupla']