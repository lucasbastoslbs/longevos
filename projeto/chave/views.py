from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView

from chave.models import Chave, ChaveDupla
from dupla.models import Dupla
from etapa.models import Etapa
from utils.decorators import LoginRequiredMixin, TreinadorRequiredMixin


class ProcessamentoChaveDetailView(LoginRequiredMixin, TreinadorRequiredMixin, DetailView):
    model = Etapa
    template_name = 'chave/chaves_etapa.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        super().get(request, *args, **kwargs)
        
        self.gerar_chaves(self.object)
        
        return super().get(request, *args, **kwargs)
    
    def criar_lista_letras(self,n):
        alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lista_letras = list(alfabeto[:n])
        return lista_letras

    def gerar_chaves(self, uma_etapa):
        print("total de duplas na etapa: ",uma_etapa.total_duplas)
        print("total de direitas na etapa: ",uma_etapa.inscritos_direita)
        print("total de esquerdas na etapa: ",uma_etapa.inscritos_esquerda)
        print("total de chaves na etapa: ",uma_etapa.total_chaves)
        
        lista_letras_chave = self.criar_lista_letras(uma_etapa.total_chaves)
        if  not Chave.objects.filter(etapa=uma_etapa).exists() and uma_etapa.inscritos_direita == uma_etapa.inscritos_esquerda and uma_etapa.total_duplas == uma_etapa.inscritos_direita:
            j = 0
            for dupla in Dupla.objects.filter(atleta_direita__etapa=uma_etapa):
                if j == uma_etapa.total_chaves:
                    j = 0
                if not Chave.objects.filter(nome=lista_letras_chave[j]):
                    chave = Chave.objects.create(nome=lista_letras_chave[j], etapa=uma_etapa)
                else:
                    chave = Chave.objects.get(nome=lista_letras_chave[j])
                
                print(f"CHAVE....{chave.nome}: Dupla: {dupla.atleta_direita.atleta.nome} + {dupla.atleta_esquerda.atleta.nome}")
                
                ChaveDupla.objects.create(chave=chave, dupla=dupla)
                j += 1
