from __future__ import unicode_literals
from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from typing import Any

from chave.models import Chave, ChaveDupla

from dupla.models import Dupla
from etapa.models import Etapa
from utils.decorators import LoginRequiredMixin, TreinadorRequiredMixin


from .forms import ChaveForm, ChaveDuplaForm

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
        # print("total de duplas na etapa: ",uma_etapa.total_duplas)
        # print("total de direitas na etapa: ",uma_etapa.inscritos_direita)
        # print("total de esquerdas na etapa: ",uma_etapa.inscritos_esquerda)
        # print("total de chaves na etapa: ",uma_etapa.total_chaves)
        
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
                
                # print(f"CHAVE....{chave.nome}: Dupla: {dupla.atleta_direita.atleta.nome} + {dupla.atleta_esquerda.atleta.nome}")
                
                ChaveDupla.objects.create(chave=chave, dupla=dupla)
                j += 1


class ChaveListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Chave
    success_url = 'chave_list'

    def get_queryset(self):
        qs = Chave.objects.all() #trouxe todas as chaves
        qs = qs.filter(Q(etapa__is_active=True))
        return qs
 

class ChaveCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Chave
    form_class = ChaveForm
    # fields = ['nome','etapa']
    success_url = 'chave_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Chave cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)


class ChaveDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Chave
    success_url = 'chave_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Chave, permissão negada!')
        return redirect(self.success_url)
    
    
class ChaveDuplaListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = ChaveDupla
    success_url = 'chavedupla_list'

    def get_queryset(self):
        qs = ChaveDupla.objects.all() #trouxe todas as chaves
        qs = qs.filter(Q(chave__etapa__is_active=True))
        return qs
 

class ChaveDuplaCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = ChaveDupla
    # fields = ['chave','dupla']
    form_class = ChaveDuplaForm
    success_url = 'chavedupla_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dupla associada à Chave com sucesso na plataforma!')
        return reverse(self.success_url)


class ChaveDuplaDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = ChaveDupla
    success_url = 'chavedupla_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Dupla na Chave, permissão negada!')
        return redirect(self.success_url)


class BuscaDuplaChaveAjaxView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        try:
            chave_id = self.request.POST.get('chave_id')
            etapa_id = self.request.POST.get('etapa_id')

            duplas = ChaveDupla.objects.all()
            if chave_id:
                duplas = duplas.filter(chave__id=chave_id)
            elif etapa_id:
                duplas = duplas.filter(chave__etapa__id=etapa_id)
            else:
                duplas = ChaveDupla.objects.none()

            lista_duplas = []
            for dupla in duplas:
                dado = {'id': dupla.id,
                        'descricao': str(dupla)}
                lista_duplas.append(dado)

            return JsonResponse({'lista_duplas':lista_duplas}, status=200)
        except Exception as e:
            retorno = {'erro': 'Erro: %s' % str(e)}
            return JsonResponse(retorno, safe=False, status=400)