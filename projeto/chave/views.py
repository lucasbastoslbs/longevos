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

    def gerar_chaves(self, uma_etapa):
        # print("total de duplas na etapa: ",uma_etapa.total_duplas)
        # print("total de direitas na etapa: ",uma_etapa.inscritos_direita)
        # print("total de esquerdas na etapa: ",uma_etapa.inscritos_esquerda)
        
        if  not Chave.objects.filter(etapa=uma_etapa).exists() and uma_etapa.inscritos_direita == uma_etapa.inscritos_esquerda and uma_etapa.total_duplas == uma_etapa.inscritos_direita:
            indice_chaves = range(1, uma_etapa.total_chaves + 1)
            j = 1
            for dupla in Dupla.objects.filter(atleta_direita__etapa=uma_etapa):
                if j == len(indice_chaves):
                    j = 1
                chave = Chave.objects.get_or_create(etapa=uma_etapa, nome=str(j))
                
                ChaveDupla.objects.create(chave=chave, dupla=dupla)
                print("asdfasdf fas ", dupla.id," chave: ", j)
                j += 1

