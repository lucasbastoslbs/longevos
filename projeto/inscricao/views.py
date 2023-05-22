from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin,  StaffRequiredMixin

from .models import Inscricao
from .forms import InscricaoForm


class InscricaoListView(LoginRequiredMixin,  ListView):
    model = Inscricao
    
class InscricaoCreateView(LoginRequiredMixin, CreateView):
    model = Inscricao    
    form_class = InscricaoForm
    success_url = 'inscricao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Inscrição regustrada com sucesso na plataforma!')
        return reverse(self.success_url)


class InscricaoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Inscricao
    form_class = InscricaoForm
    success_url = 'inscricao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados da Inscrição atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class InscricaoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Inscricao
    success_url = 'inscricao_list'

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
            messages.error(request, 'Há dependências ligadas a essa Inscrição, permissão negada!')
        return redirect(self.success_url)