from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, Sum
import json
from .models import Ambito, Ubigeo, CentroVotacion, GrupoVotacion, AgrupacionPolitica, APoliticaUbigeo, Acta


def index(request):
	ambitos = Ambito.objects.all().exclude(Q(pk = 1) | Q(pk = 2) | Q(pk = 6)).order_by("pk")
	regiones = Ubigeo.objects.filter(codDep = '06', codPro = '00', codDis="00")
	provincias = Ubigeo.objects.filter(codDep = "06", codDis = "00").exclude(codPro = '00').order_by("nombre")


	if (request.GET.get("ambito") and request.GET.get("provincia") and request.GET.get("distrito")) :
		distrito = Ubigeo.objects.get(pk = request.GET.get("distrito"))
		centrosVotacion = CentroVotacion.objects.filter(ubigeo = distrito).order_by("nombre")
		return render(request, "elecciones_app/centrosVotacion.html", locals())
	

	else:
		return render(request, "elecciones_app/index.html", locals())

def gruposVotacion(request, idCentroVotacion):
	centroVotacion = CentroVotacion.objects.get(pk = idCentroVotacion)

	gruposVotacion = GrupoVotacion.objects.filter(centroVotacion = centroVotacion)
	totalElectores = gruposVotacion.aggregate(cantidad = Sum('electoresHabiles'))

	return render(request, "elecciones_app/gruposVotacion.html", locals())


def distritos(request, idProv):
	provincia = Ubigeo.objects.get(pk = idProv)
	distritos = Ubigeo.objects.filter(codDep= '06', codPro = provincia.codPro).exclude(codDis = '00').order_by("nombre")
	return render(request, "elecciones_app/distritos.html", locals())


def registrarActa(request, idGrupoVotacion, idDistrito, idAmbito):
	grupoVotacion = GrupoVotacion.objects.get(pk = idGrupoVotacion)
	distrito = Ubigeo.objects.get(pk = idDistrito)
	ambito = Ambito.objects.get(pk = idAmbito)

	if ambito.nombre == "Regional":
		agrupacionesPoliticas = AgrupacionPolitica.objects.filter(
			ubigeo__pk = idDistrito,
			apoliticaubigeo__ambito__pk = 1
		)


		actas = Acta.objects.filter(
			Q(APoliticaUbigeo__ubigeo = distrito),
			Q(APoliticaUbigeo__ambito__pk = 1) | Q(APoliticaUbigeo__ambito__pk = 2),
			Q(grupoVotacion = grupoVotacion)
		).order_by("APoliticaUbigeo__ambito__pk")

		template = "elecciones_app/registrarActa.html"

	# elif ambito.nombre == "Municipal Provincial":
	else:
		agrupacionesPoliticas = AgrupacionPolitica.objects.filter(
			ubigeo__pk = idDistrito,
			apoliticaubigeo__ambito__pk = idAmbito
		)

		actas = Acta.objects.filter(
			APoliticaUbigeo__ubigeo = distrito,
			APoliticaUbigeo__ambito__pk = ambito.pk,
			grupoVotacion = grupoVotacion
		)
		template = "elecciones_app/registrarActaProvincial.html"

	return render(request, template, locals())


def registrarActaSubmit(request):
	votos = json.loads(request.POST.get("json"))
	centroVotacionId = int(request.POST.get("centroVotacion"))
	grupoVotacionId = int(request.POST.get("grupoVotacion"))

	response_data  = {}
	response_data["centroVotacion"] = centroVotacionId
	try:
		for voto in votos:
			# Guardamos votos en la base de datos
			acta = Acta.objects.get(pk = voto["actaId"])
			acta.numVotos = voto["numVotos"]
			acta.save()

		grupoVotacion = GrupoVotacion.objects.get(pk = grupoVotacionId)
		grupoVotacion.contabilizado = True
		grupoVotacion.save()

		response_data['estado'] = 1
		response_data['message'] = "Datos guardados correctamente"
		
	except Exception, e:
		response_data['estado'] = 0
		response_data['message'] = "Error: " + str(e)

	return HttpResponse(json.dumps(response_data), content_type="application/json")
	



