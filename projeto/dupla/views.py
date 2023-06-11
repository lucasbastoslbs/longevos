from __future__ import unicode_literals

from django.db.models import Q
from django.contrib import messages

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin,  TreinadorRequiredMixin

from .models import Dupla
from .forms import DuplaForm, BuscaDuplaForm


class DuplaListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Dupla
    template_name = 'dupla/dupla_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaDuplaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaDuplaForm()
        return context

    def get_queryset(self):
        qs = Dupla.objects.all() #trouxe todas as inscrições
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaDuplaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaDuplaForm()

        if form.is_valid():
            atleta = form.cleaned_data.get('atleta')
            etapa = form.cleaned_data.get('etapa')
            # posicao = form.cleaned_data.get('posicao')

            if etapa:
                qs = qs.filter(Q(atleta_direita__etapa=etapa))

            if atleta:
                qs = qs.filter(Q(atleta_direita__atleta__nome__icontains=atleta) | Q(atleta_direita__atleta__apelido__icontains=atleta) | Q(atleta_esquerda__atleta__nome__icontains=atleta) | Q(atleta_esquerda__atleta__apelido__icontains=atleta))

            # if posicao:
            #     qs = qs.filter(Q(atleta_direita__atleta__posicao__icontains=posicao) | Q(atleta_esquerda__atleta__posicao__icontains=posicao))
            
        return qs
 

class DuplaCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Dupla
    form_class = DuplaForm
    # fields = ['atleta_direita', 'atleta_esquerda']
    success_url = 'dupla_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dupla cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)


class DuplaUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Dupla
    form_class = DuplaForm
    # fields = ['atleta_direita', 'atleta_esquerda', 'pontuacao_dupla']
    success_url = 'dupla_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados da Dupla atualizados com sucesso na plataforma!')
        return reverse(self.success_url) 


class DuplaDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Dupla
    success_url = 'dupla_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.atleta_direita.com_dupla = False
            self.object.atleta_esquerda.com_dupla = False
            self.object.atleta_direita.save()
            self.object.atleta_esquerda.save()
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Dupla, permissão negada!')
        return redirect(self.success_url)