from django.conf.urls import url

from .views import DuplaListView, DuplaCreateView
from .views import DuplaUpdateView, DuplaDeleteView


urlpatterns = [
	url(r'list/$', DuplaListView.as_view(), name='dupla_list'),
	url(r'cad/$', DuplaCreateView.as_view(), name='dupla_create'),
	url(r'(?P<pk>\d+)/$', DuplaUpdateView.as_view(), name='dupla_update'),
	url(r'(?P<pk>\d+)/delete/$', DuplaDeleteView.as_view(), name='dupla_delete'), 
]
