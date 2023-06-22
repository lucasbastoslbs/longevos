from __future__ import unicode_literals

import os

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin,  TreinadorRequiredMixin

from .models import Foto


class FotoListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Foto
    template_name = 'foto/foto_list.html'

    
class FotoCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Foto    
    fields = ['titulo', 'arquivo']
    success_url = 'foto_list'
    success_message = 'Foto registrada com sucesso na plataforma!'
        
    def form_valid(self, form):
        formulario = form.save(commit=False)
        #verificar se os arquivos carregados são png ou jpg
        if (not Imagem.so_imagem(self, formulario)):
            messages.warning(self.request, 'Sistema suporta SOMENTE png!')
            return super(FotoCreateView, self).form_invalid(form)
        
        formulario.save()
        return super().form_valid(form)
        
   
class FotoUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Foto    
    fields = ['titulo', 'arquivo']
    success_url = 'foto_list'
    
    def form_valid(self, form):
        formulario = form.save(commit=False)
        #verificar se os arquivos carregados são png   
        if (not Imagem.so_imagem(self, formulario)):
            messages.warning(self.request, 'Sistema suporta SOMENTE png!')
            return super(FotoUpdateView, self).form_invalid(form)
        
        formulario.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Foto atualizada com sucesso na plataforma!')
        return reverse(self.success_url)


class FotoDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Foto
    success_url = 'foto_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        
        try:
            self.object.delete()            
        except Exception as e:
            messages.error(request, 'Há dependências ligadas a essa Foto, permissão negada!')
        return redirect(self.success_url)
    
class Imagem:
    @staticmethod
    def so_imagem(self, formulario):
        file_name, file_extension = os.path.splitext(str(formulario.arquivo))
        if (formulario.arquivo and file_extension != '.png'):
            return False
        return True