from __future__ import unicode_literals

from django.contrib import messages

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin,  TreinadorRequiredMixin

from .models import Dupla
from .forms import DuplaForm


class DuplaListView(LoginRequiredMixin, ListView):
    model = Dupla
 

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