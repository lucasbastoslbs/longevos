from django.conf.urls import url

from .views import ProcessamentoChaveDetailView


urlpatterns = [
	url(r'(?P<pk>\d+)/processamento-chaves-etapa/$', ProcessamentoChaveDetailView.as_view(), name='processamento_chaves_etapa'),
]
