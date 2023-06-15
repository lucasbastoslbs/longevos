from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from mail_templated import EmailMessage

from utils.decorators import LoginRequiredMixin, AtletaRequiredMixin

from inscricao.models import Inscricao
from usuario.models import Usuario

from .forms import InscricaoForm


class HomeView(LoginRequiredMixin, AtletaRequiredMixin, TemplateView):
    template_name = 'appatleta/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['avisos'] = Aviso.ativos.filter(destinatario__in=[self.request.user.tipo, 'TODOS'])[0:2]
    #     return context

class AboutView(LoginRequiredMixin, AtletaRequiredMixin, TemplateView):
    template_name = 'appatleta/about.html'
    

class DadosAtletaUpdateView(LoginRequiredMixin, AtletaRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'appatleta/dados_atleta_form.html'
    fields = ['nome', 'apelido', 'data_nascimento', 'email', 'posicao']
    success_url = 'appatleta_home'

    def get_object(self, queryset=None):
        return self.request.user
     
    def get_success_url(self):
        messages.success(self.request, 'Seus dados foram alterados com sucesso!')
        return reverse(self.success_url)


class InscricaoListView(LoginRequiredMixin, AtletaRequiredMixin, ListView):
    model = Inscricao
    template_name = 'appatleta/inscricao_list.html'
   
    def get_queryset(self):
        queryset = super(InscricaoListView, self).get_queryset()
        return queryset.filter(atleta = self.request.user)


class InscricaoCreateView(LoginRequiredMixin, AtletaRequiredMixin, CreateView):
    model = Inscricao
    template_name = 'appatleta/inscricao_form.html'
    form_class = InscricaoForm
    success_url = 'appatleta_inscricao_list'
    
    def get_initial(self):
        initials = super().get_initial()
        initials['usuario'] = Usuario.objects.get(id=self.request.user.id)
        return initials
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atleta'] = Usuario.objects.get(id=self.request.user.id)
        return context

    def form_valid(self, form):
        try:
            formulario = form.save(commit=False)
            formulario.atleta = self.request.user
            
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

            try:
                """ enviar e-mail para atleta """
                message = EmailMessage('usuario/email/inscricao_atleta.html', {'inscricao': self.object},
                        settings.EMAIL_HOST_USER, to=[self.object.atleta.email])
                message.send()
            except:
                # alterar para outro tipo de requisição http
                messages.warning(self.request, "Inscrição realizada mas SEM NOTIFICAÇÃO POR EMAIL AO ATLETA!!")
                
            formulario.etapa.save()
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, 'Erro ao inscrever-se na etapa. Verifique se você já não está inscrito na etapa')
            return super().form_invalid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Inscrição realizada com sucesso na plataforma!')
        return reverse(self.success_url)
    

class InscricaoDeleteView(LoginRequiredMixin, AtletaRequiredMixin, DeleteView):
    model = Inscricao
    template_name = 'appatleta/inscricao_confirm_delete.html'
    success_url = 'appatleta_inscricao_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        etapa_atual = self.object.etapa
        posicao = self.object.posicao_etapa
        
        try:
            self.object.delete()
            
            if (posicao == "DIREITA"):
                etapa_atual.inscritos_direita -= 1
            
            if (posicao == "ESQUERDA"):
                etapa_atual.inscritos_esquerda -= 1
            
            etapa_atual.save()
            
        except Exception as e:
            messages.error(request, 'Já não é mais possível cancelar a inscrição, permissão negada!')
        return redirect(self.success_url)        


