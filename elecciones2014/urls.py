from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'elecciones_app.views.index', name='home'),
    url(r'^distritos/(\d+)$', 'elecciones_app.views.distritos', name='distritos'),
    url(r'^gruposVotacion/(\d+)$', 'elecciones_app.views.gruposVotacion', name='gruposVotacion'),
    url(r'^registrarActa/(\d+)/(\d+)/(\d+)$', 'elecciones_app.views.registrarActa', name='registrarActa'),
    url(r'^registrarActaSubmit/$', 'elecciones_app.views.registrarActaSubmit', name='registrarActaSubmit'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^cargarApoliticasUbigeo$', 'elecciones_app.views.cargarApoliticasUbigeo', name='carga1'),
    url(r'^cargarActas$', 'elecciones_app.views.cargarActas', name='carga2'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
