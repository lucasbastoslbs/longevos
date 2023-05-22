from django import forms
from .models import Usuario

  
class BuscaUsuarioForm(forms.Form):
    pesquisa = forms.CharField(label='Digite algo para pesquisar', required=False)
    