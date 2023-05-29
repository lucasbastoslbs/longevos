from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin,  StaffRequiredMixin, TreinadorRequiredMixin

from .models import Inscricao
from .forms import InscricaoForm


class InscricaoListView(LoginRequiredMixin,  ListView):
    model = Inscricao
    
class InscricaoCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Inscricao    
    form_class = InscricaoForm
    success_url = 'inscricao_list'
    success_message = 'Inscrição registrada com sucesso na plataforma!'
    

    # success_url = reverse_lazy('aplicativo:fonte_list')
    
    def form_valid(self, form):
        formulario = form.save(commit=False)
        
        # print("Vagas: ", formulario.etapa.total_duplas * 2)
        # print("Direita: ", formulario.etapa.inscritos_direita)
        # print("Esquerda: ", formulario.etapa.inscritos_esquerda)
        # print("Diferenca: ",(formulario.etapa.total_duplas * 2) - (formulario.etapa.inscritos_direita + formulario.etapa.inscritos_esquerda))
        
        if ((formulario.etapa.total_duplas * 2) - (formulario.etapa.inscritos_direita + formulario.etapa.inscritos_esquerda) == 0):
            messages.error(self.request,"Não há mais vagas para nenhuma posição. Inscrição NÃO realizada. Aguarde liberar uma vaga!!!")  
            return super().form_invalid(form)
        elif (formulario.posicao_etapa == 'DIREITA'):
            if (formulario.etapa.total_duplas == formulario.etapa.inscritos_direita):
                messages.error(self.request,"Não há mais vagas para DIREITA, somente para ESQUERDA ")  
                return super().form_invalid(form)
            formulario.etapa.inscritos_direita += 1
        else:
            if (formulario.etapa.total_duplas == formulario.etapa.inscritos_esquerda):
                messages.error(self.request,"Não há mais vagas para ESQUERDA, somente para DIREITA")  
                return super().form_invalid(form)
            formulario.etapa.inscritos_esquerda += 1


        print("ENTREI AQUI....")
        formulario.etapa.save()
        formulario.save()
        return super().form_valid(form)
        

    # def get_success_url(self):
    #     messages.success(self.request, 'Inscrição registrada com sucesso na plataforma!')
    #     return reverse(self.success_url)


class InscricaoUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Inscricao
    form_class = InscricaoForm
    success_url = 'inscricao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados da Inscrição atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class InscricaoDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Inscricao
    success_url = 'inscricao_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        
        try:
            if (self.object.posicao_etapa == "DIREITA"):
                self.object.etapa.inscritos_direita -= 1
            
            if (self.object.posicao_etapa == "ESQUERDA"):
                self.object.etapa.inscritos_esquerda -= 1
            
            self.object.etapa.save()
            self.object.delete()
            
        except Exception as e:
            messages.error(request, 'Há dependências ligadas a essa Inscrição, permissão negada!')
        return redirect(self.success_url)