from django.shortcuts import render
from django.db.models import Q
import json
from .models import Ambito, Ubigeo, CentroVotacion, GrupoVotacion, AgrupacionPolitica, Acta


def index(request):
	ambitos = Ambito.objects.all()
	regiones = Ubigeo.objects.filter(codDep = '06', codPro = '00', codDis="00")
	provincias = Ubigeo.objects.filter(codDep = "06", codDis = "00").exclude(codPro = '00')

	if (request.GET.get("ambito") and request.GET.get("provincia") and request.GET.get("distrito")) :
		distrito = Ubigeo.objects.get(pk = request.GET.get("distrito"))
		centrosVotacion = CentroVotacion.objects.filter(ubigeo = distrito)
		return render(request, "elecciones_app/centrosVotacion.html", locals())
	
	else:
		return render(request, "elecciones_app/index.html", locals())

def gruposVotacion(request, idCentroVotacion):
	centroVotacion = CentroVotacion.objects.get(pk = idCentroVotacion)
	gruposVotacion = GrupoVotacion.objects.filter(centroVotacion = centroVotacion)
	return render(request, "elecciones_app/gruposVotacion.html", locals())


def distritos(request, idProv):
	provincia = Ubigeo.objects.get(pk = idProv)
	distritos = Ubigeo.objects.filter(codDep= '06', codPro = provincia.codPro).exclude(codDis = '00')
	return render(request, "elecciones_app/distritos.html", locals())


def registrarActa(request, idGrupoVotacion, idDistrito, idAmbito):
	grupoVotacion = GrupoVotacion.objects.get(pk = idGrupoVotacion)
	# centroVotacion = CentroVotacion.objects.filter(grupovotacion__id = idGrupoVotacion)
	distrito = Ubigeo.objects.get(pk = idDistrito)
	ambito = Ambito.objects.get(pk = idAmbito)


	agrupacionesPoliticas = AgrupacionPolitica.objects.filter(ubigeo__pk = idDistrito, acta__ambito__pk = idAmbito)

	actas = Acta.objects.filter(
		Q(ubigeo = distrito),
		Q(ambito__pk = 1) | Q(ambito__pk = 2),
		Q(grupoVotacion = grupoVotacion)
	).order_by("ambito__pk")

	if ambito.nombre == "Presidente Regional":
		return render(request, "elecciones_app/registrarActa.html", locals())


def registrarActaSubmit(request):
	votos = json.loads(request.POST.get("json"))
	for voto in votos:
		# print voto["actaId"] + " -> " + voto["numVotos"]
		# Guardamos votos en la base de datos
		acta = Acta.objects.get(pk = voto["actaId"])
		acta.numVotos = voto["numVotos"]
		acta.save()

	return render(request, "elecciones_app/registrarActa.html", locals())



