from django import forms

  
class BuscaUsuarioForm(forms.Form):
    pesquisa = forms.CharField(label='Digite algo para pesquisar', required=False)
    