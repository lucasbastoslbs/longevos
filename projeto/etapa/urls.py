from django.conf.urls import url

from .views import EtapaListView, EtapaCreateView
from .views import EtapaUpdateView, EtapaDeleteView


urlpatterns = [
	url(r'list/$', EtapaListView.as_view(), name='etapa_list'),
	url(r'cad/$', EtapaCreateView.as_view(), name='etapa_create'),
	url(r'(?P<pk>\d+)/$', EtapaUpdateView.as_view(), name='etapa_update'),
	url(r'(?P<pk>\d+)/delete/$', EtapaDeleteView.as_view(), name='etapa_delete'), 
]
