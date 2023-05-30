from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('core.urls')),
    url(r'usuario/', include('usuario.urls')),
    url(r'etapa/', include('etapa.urls')),
    url(r'inscricao/', include('inscricao.urls')),
    url(r'dupla/', include('dupla.urls')),
    url(r'chave/', include('chave.urls')),
   
    url(r'^accounts/', include('django.contrib.auth.urls')),
]