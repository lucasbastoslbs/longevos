from django.conf.urls import url

from .views import  JogoListView, JogoCreateView, JogoUpdateView, JogoDeleteView
# from .views import ChaveDuplaListView, ChaveDuplaCreateView, ChaveDuplaDeleteView


urlpatterns = [
	# url(r'duplanachave/list/$', ChaveDuplaListView.as_view(), name='chavedupla_list'),
	# url(r'duplanachave/cad/$', ChaveDuplaCreateView.as_view(), name='chavedupla_create'),
	# url(r'duplanachave/(?P<pk>\d+)/delete/$', ChaveDuplaDeleteView.as_view(), name='chavedupla_delete'), 
 
	url(r'list/$', JogoListView.as_view(), name='jogo_list'),
	url(r'cad/$', JogoCreateView.as_view(), name='jogo_create'),
 	url(r'(?P<pk>\d+)/$', JogoUpdateView.as_view(), name='jogo_update'),
	url(r'(?P<pk>\d+)/delete/$', JogoDeleteView.as_view(), name='jogo_delete'), 
 
	# url(r'(?P<pk>\d+)/processamento-jogos-chave-etapa/$', ProcessamentoJogoDetailView.as_view(), name='processamento_jogos_chaves_etapa'),
]
