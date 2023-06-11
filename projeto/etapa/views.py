from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, TreinadorRequiredMixin

from .models import Etapa


class EtapaListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Etapa
 

class EtapaCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Etapa
    fields = ['grupo','data', 'local', 'total_duplas', 'total_chaves', 'is_active']
    success_url = 'etapa_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Etapa cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)


class EtapaUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Etapa
    fields = ['grupo','data', 'local', 'total_duplas', 'total_chaves', 'is_active']
    success_url = 'etapa_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados da Etapa atualizados com sucesso na plataforma!')
        return reverse(self.success_url) 


class EtapaDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Etapa
    success_url = 'etapa_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Etapa, permissão negada!')
        return redirect(self.success_url)