from django.conf.urls import url

from .views import ProcessamentoChaveDetailView, ChaveListView, ChaveCreateView, ChaveDeleteView


urlpatterns = [
	url(r'list/$', ChaveListView.as_view(), name='chave_list'),
	url(r'cad/$', ChaveCreateView.as_view(), name='chave_create'),
	url(r'(?P<pk>\d+)/delete/$', ChaveDeleteView.as_view(), name='chave_delete'), 
	url(r'(?P<pk>\d+)/processamento-chaves-etapa/$', ProcessamentoChaveDetailView.as_view(), name='processamento_chaves_etapa'),
]
