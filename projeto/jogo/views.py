from __future__ import unicode_literals
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from typing import Any

from jogo.models import Jogo

from utils.decorators import LoginRequiredMixin, TreinadorRequiredMixin

from .forms import JogoForm


class JogoListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Jogo
    success_url = 'jogo_list'

    def get_queryset(self):
        qs = Jogo.objects.all() #trouxe todas as etapas
        qs = qs.filter(Q(chave__etapa__is_active=True))
        return qs
 

class JogoCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Jogo
    form_class = JogoForm    
    success_url = 'jogo_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Jogo cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)
    
    
class JogoUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Jogo
    form_class = JogoForm    
    success_url = 'jogo_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Jogo alterado com sucesso na plataforma!')
        return reverse(self.success_url)


class JogoDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Jogo
    success_url = 'jogo_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse Jogo, operação negada!')
        return redirect(self.success_url)
    
    
