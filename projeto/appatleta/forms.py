from django import forms

from etapa.models import Etapa
from inscricao.models import Inscricao
# from usuario.models import Usuario


class InscricaoForm(forms.ModelForm):
    etapa = forms.ModelChoiceField(label='Etapa', queryset=Etapa.etapas_ativas.all())
    # atleta = forms.ModelChoiceField(label='Atleta', queryset=Usuario.atletas.all())
   

    class Meta:
        model = Inscricao
        fields = ['etapa',  'posicao_etapa']