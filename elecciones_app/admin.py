from django.contrib import admin
from .models import Ambito, Ubigeo, CentroVotacion, AgrupacionPolitica, GrupoVotacion, Acta


class UbigeoAdmin(admin.ModelAdmin):
	list_display = ("codDep", "codPro", "codDis", "nombre", )

admin.site.register(Ambito)
admin.site.register(Ubigeo, UbigeoAdmin)
admin.site.register(CentroVotacion)
admin.site.register(AgrupacionPolitica)
admin.site.register(GrupoVotacion)
admin.site.register(Acta)
