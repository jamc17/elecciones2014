from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'elecciones_app.views.index', name='home'),
    url(r'^distritos/(\d+)/(\d+)$', 'elecciones_app.views.distritos', name='distritos'),
    url(r'^gruposVotacion/(\d+)/(\d+)/(\d+)$', 'elecciones_app.views.gruposVotacion', name='gruposVotacion'),
    url(r'^registrarActa/(\d+)/(\d+)/(\d+)$', 'elecciones_app.views.registrarActa', name='registrarActa'),
    url(r'^registrarActaSubmit/$', 'elecciones_app.views.registrarActaSubmit', name='registrarActaSubmit'),
    
	url(r'^getResumenCentroVotacion/(\d+)/(\d+)$', 'elecciones_app.views.getResumenCentroVotacion', name='resumenCentroVotacion'),

    url(r'^login/$', 'elecciones_app.views.viewLogin', name='viewLogin'),
    url(r'^logout/$', 'elecciones_app.views.viewLogout', name='viewLogout'),

    url(r'^reportes$', 'elecciones_app.views.reportes', name='reportes'),
    url(r'^getReporteUbigeo/(\d+)/(\d+)/(\d+)$', 'elecciones_app.views.getReporteUbigeo', name='getReporteUbigeo'),
    
	# Acciones Administrativas
    url(r'^cargarApoliticasUbigeo$', 'elecciones_app.views.cargarApoliticasUbigeo', name='carga1'),
    url(r'^cargarActas$', 'elecciones_app.views.cargarActas', name='carga2'),

    url(r'^cargaTotalesMunicipales$', 'elecciones_app.views.cargaTotalesMunicipales', name='cargaTotalesMunicipales'),

    url(r'^cargaActasTotalesMunicipales$', 'elecciones_app.views.cargaActasTotalesMunicipales', name='cargaActasTotalesMunicipales'),

    url(r'^resetDatabaseEleccionesRM$', 'elecciones_app.views.resetDatabaseEleccionesRM', name='resetDatabaseEleccionesRM'),
    
    

    url(r'^limpiaActasSanJuan$', 'elecciones_app.views.limpiaActasSanJuan', name='limpiarActas'),
    url(r'^cargaActasSanJuan$', 'elecciones_app.views.cargaAPoliticasUbigeoSanJuan', name='cargaActasUbigeo'),

    

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
