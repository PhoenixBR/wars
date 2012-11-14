from django.conf.urls import patterns, include, url
from django.conf import settings

import views.crimes
import views.perfil
import views.loja
import views.site

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'views.perfil.index', name='pagina_inicial'), #pagina inicial
    url(r'^AdicionarStatus/(\w+)', 'views.perfil.adicionarStatus'),
    url(r'^equipar/arma/(?P<nr_item>\d+)', 'views.perfil.equipar_arma'),
    url(r'^equipar/armadura/(?P<nr_item>\d+)', 'views.perfil.equipar_armadura'),
    
    url(r'^loja/$', 'views.loja.loja', name='pagina_da_loja'),
    url(r'^loja/vender/arma/(?P<nr_item>\d+)', 'views.loja.vender_arma'),
    url(r'^loja/comprar/arma/(?P<nr_item>\d+)', 'views.loja.comprar_arma'),
    url(r'^loja/vender/armadura/(?P<nr_item>\d+)', 'views.loja.vender_armadura'),
    url(r'^loja/comprar/armadura/(?P<nr_item>\d+)', 'views.loja.comprar_armadura'),

    url(r'^crimes/$', 'views.crimes.crimes', name='pagina_de_crimes'),
    url(r'^crimes/cometer/(\d+)', 'views.crimes.cometer_crime'),

    url(r'^login/$', "django.contrib.auth.views.login", 
                                {"template_name": "logar.html"}), # pagina de cadastro
    url(r'^logout/', "django.contrib.auth.views.logout_then_login", 
                                {"login_url": '/login/'}),

    url(r'^registrar/$', 'views.site.registrar', name='pagina_de_registro'), # pagina de cadastro
    url(r'^malicia_refresh/$', 'views.site.malicia_refresh'),
    url(r'^malicia_hospital/$', 'views.site.malicia_hospital'),
    url(r'^rank/$', 'views.site.rank', name='pagina_de_rank'),

    url(r'^luta/$', 'views.lutas.alvos', name='pagina_de_luta'),
    url(r'^luta/atacar/(\d+)', 'views.lutas.atacar'), 

    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^arquivos/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),)
