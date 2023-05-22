from django.conf.urls import url

from .views import InscricaoListView, InscricaoCreateView
from .views import InscricaoUpdateView, InscricaoDeleteView


urlpatterns = [
 	url(r'list/$', InscricaoListView.as_view(), name='inscricao_list'),
	url(r'cad/$', InscricaoCreateView.as_view(), name='inscricao_create'),
	url(r'(?P<pk>\d+)/$', InscricaoUpdateView.as_view(), name='inscricao_update'),
	url(r'(?P<pk>\d+)/delete/$', InscricaoDeleteView.as_view(), name='inscricao_delete'), 
]
