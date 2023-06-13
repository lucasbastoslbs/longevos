from django.conf.urls import url

from .views import ProcessamentoChaveDetailView, ChaveListView, ChaveCreateView, ChaveDeleteView, ChaveDuplaListView, ChaveDuplaCreateView, ChaveDuplaDeleteView


urlpatterns = [
	url(r'duplanachave/list/$', ChaveDuplaListView.as_view(), name='chavedupla_list'),
	url(r'duplanachave/cad/$', ChaveDuplaCreateView.as_view(), name='chavedupla_create'),
	url(r'duplanachave/(?P<pk>\d+)/delete/$', ChaveDuplaDeleteView.as_view(), name='chavedupla_delete'), 
 
	url(r'list/$', ChaveListView.as_view(), name='chave_list'),
	url(r'cad/$', ChaveCreateView.as_view(), name='chave_create'),
	url(r'(?P<pk>\d+)/delete/$', ChaveDeleteView.as_view(), name='chave_delete'), 
 
	url(r'(?P<pk>\d+)/processamento-chaves-etapa/$', ProcessamentoChaveDetailView.as_view(), name='processamento_chaves_etapa'),
]
