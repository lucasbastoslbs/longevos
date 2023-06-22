from django.conf.urls import url

from .views import FotoListView, FotoCreateView
from .views import FotoUpdateView, FotoDeleteView


urlpatterns = [
 	url(r'list/$', FotoListView.as_view(), name='foto_list'),
	url(r'cad/$', FotoCreateView.as_view(), name='foto_create'),
	url(r'(?P<pk>\d+)/$', FotoUpdateView.as_view(), name='foto_update'),
	url(r'(?P<pk>\d+)/delete/$', FotoDeleteView.as_view(), name='foto_delete'), 
]
