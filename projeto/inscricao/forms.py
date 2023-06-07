from django import forms

from usuario.models import Usuario

from .models import Inscricao
from etapa.models import Etapa


class InscricaoForm(forms.ModelForm):
    etapa = forms.ModelChoiceField(label='Etapa', queryset=Etapa.etapas_ativas.all())
    atleta = forms.ModelChoiceField(label='Atleta', queryset=Usuario.atletas.all())
   

    class Meta:
        model = Inscricao
        fields = ['etapa', 'atleta', 'posicao_etapa']
    

class BuscaInscricaoForm(forms.Form):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    POSICAO = (
        (None,'-------------'),
        ('DIREITA', 'Direita'),
        ('ESQUERDA', 'Esquerda' ),
        ('AMBAS', 'Ambas' ),
    )
    atleta = forms.CharField(label='Digite dados do atleta', required=False)
    posicao = forms.ChoiceField(label='Selecione a posição do atleta', choices=POSICAO, required=False)
    etapa = forms.ModelChoiceField(label='Etapa', queryset=Etapa.etapas_ativas.all(), required=False)
    
