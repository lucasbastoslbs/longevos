from __future__ import unicode_literals
from django.conf.urls import url

from core.views import HomeRedirectView

from .views import (DadosAtletaUpdateView, 
                    InscricaoListView, InscricaoCreateView, 
                    HomeView, AboutView)

urlpatterns = [
   url(r'^home$', HomeView.as_view(), name='appatleta_home'), 
   # url(r'^$', HomeRedirectView.as_view(), name='home_redirect'),
   url(r'^about$', AboutView.as_view(), name='appatleta_about'),

   url(r'^meus-dados/$', DadosAtletaUpdateView.as_view(), name='appatleta_dados_update'),

   url(r'^minhas-inscricoes$', InscricaoListView.as_view(), name='appatleta_inscricao_list'),
   url(r'^minhas-inscricoes/cad/$', InscricaoCreateView.as_view(), name='appatleta_inscricao_create'),
   
]
