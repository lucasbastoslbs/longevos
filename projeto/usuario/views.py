from django.contrib import messages
from django.db.models import Q

from django.shortcuts import redirect
from django.urls import reverse

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, TreinadorRequiredMixin

from .models import Usuario
from .forms import BuscaUsuarioForm


class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dado filtrando
            context['form'] = BuscaUsuarioForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            context['form'] = BuscaUsuarioForm()
        return context

    def get_queryset(self):
        qs = Usuario.objects.all()
        
        if self.request.GET:
            #quando ja tem dado filtrando
            form = BuscaUsuarioForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            form = BuscaUsuarioForm()

        if form.is_valid():
            pesquisa = form.cleaned_data.get('pesquisa')

            if pesquisa:
                qs = qs.filter(Q(nome__icontains=pesquisa) | Q(apelido__icontains=pesquisa) | Q(posicao__icontains=pesquisa))
            
        return qs


class UsuarioCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Usuario
    fields = ['tipo', 'grupo', 'nome', 'apelido', 'data_nascimento', 'posicao', 'pontuacao', 'qtd_etapas_jogadas', 'is_active', 'celular', 'email','password'] 
    
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Usuário cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class UsuarioUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Usuario
    fields = ['tipo', 'grupo', 'nome', 'apelido', 'data_nascimento','posicao', 'pontuacao', 'qtd_etapas_jogadas', 'is_active', 'celular', 'email'] 
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados do usuário atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class UsuarioDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Usuario
    success_url = 'usuario_list'

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
            messages.error(request, 'Há dependências ligadas à esse usuário, permissão negada!')
        return redirect(self.success_url)

