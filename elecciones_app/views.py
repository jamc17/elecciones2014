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


def getResumenCentroVotacion(request, idCentroVotacion, idAmbito):
	centroVotacion = CentroVotacion.objects.get(pk = idCentroVotacion)
	ubigeo = centroVotacion.ubigeo
	ambito = Ambito.objects.get(pk =idAmbito)
	
	if ambito.nombre == "Regional":
		
		apus = ubigeo.apoliticaubigeo_set.filter(Q(ambito__pk = 1)| Q(ambito__pk = 2))

	return render(request, "elecciones_app/resumenCentroVotacion.html", locals())


def distritos(request, idProv, idAmbito):
	provincia = Ubigeo.objects.get(pk = idProv)
	ambito = Ambito.objects.get(pk = idAmbito)
	distritos = Ubigeo.objects.filter(codDep= '06', codPro = provincia.codPro).exclude(codDis = '00').order_by("nombre")

	if ambito.nombre == "Municipal Provincial":
		distritos = distritos.filter(distritoCapital = True)

	elif ambito.nombre == "Municipal Distrital":
		distritos = distritos.filter(distritoCapital = False)
	

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

	elif ambito.nombre == "Municipal Provincial":
	# else:
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

	elif ambito.nombre == "Municipal Distrital":
		agrupacionesPoliticas = AgrupacionPolitica.objects.filter(
			Q(ubigeo__pk = idDistrito),
			Q(apoliticaubigeo__ambito__pk = idAmbito)
		)

		agrupacionesPoliticasProv = AgrupacionPolitica.objects.filter(
			Q(ubigeo__pk = idDistrito),
			Q(apoliticaubigeo__ambito__pk = 4)
		)

		if agrupacionesPoliticas.count() < agrupacionesPoliticasProv.count():
			agrupacionesPoliticas = agrupacionesPoliticasProv


		actas = Acta.objects.filter(
			Q(APoliticaUbigeo__ubigeo = distrito),
			Q(APoliticaUbigeo__ambito__pk = ambito.pk) | Q(APoliticaUbigeo__ambito__pk = 4),
			Q(grupoVotacion = grupoVotacion)
		).order_by("APoliticaUbigeo__ambito__pk")
		template = "elecciones_app/registrarActaDistrital.html"

	return render(request, template, locals())


def registrarActaSubmit(request):
	votos = json.loads(request.POST.get("json"))
	centroVotacionId = int(request.POST.get("centroVotacion"))
	grupoVotacionId = int(request.POST.get("grupoVotacion"))

	action = request.POST.get("action")

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
		if action == "resetActa":
			grupoVotacion.contabilizado = False
		
		grupoVotacion.save()

		response_data['estado'] = 1
		response_data['message'] = "Datos guardados correctamente"
		
	except Exception, e:
		response_data['estado'] = 0
		response_data['message'] = "Error: " + str(e)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def cargarApoliticasUbigeo(request):
	aps = AgrupacionPolitica.objects.filter(
		Q(pk = 12) | Q(pk = 20) | Q(pk = 26) | Q(pk = 28) |Q(pk = 29) | Q(pk = 30) | Q(pk = 32) | Q(pk = 34)| Q(pk = 35)| Q(pk = 36)| Q(pk = 37) | Q(pk = 38)
		)
	ubigeos = Ubigeo.objects.exclude(codDis = "00")
	ambitos = Ambito.objects.filter(
		Q(pk = 1) | Q(pk = 2)
		)
	try:
		for ambito in ambitos:
			for ap in aps:
				for ubigeo in ubigeos:
					apu = APoliticaUbigeo()
					apu.ubigeo = ubigeo
					apu.agrupacionPolitica = ap
					apu.ambito = ambito
					apu.save()

		return HttpResponse("Dataos cargados correctamente")

	except Exception, e:
		raise e


def cargarActas(request):
	# gruposVotacion = GrupoVotacion.objects.all()
	# apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 1) | Q(ambito_id = 2) | Q(ambito_id = 5))
	apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 4))
	# apus = APoliticaUbigeo.objects.filter()
	
	for apu in apus:
		ubigeo = apu.ubigeo
		locales = ubigeo.centrovotacion_set.all()
		for local in locales:
			mesas = local.grupovotacion_set.all()
			for mesa in mesas:
				acta = Acta()
				acta.APoliticaUbigeo = apu
				acta.grupoVotacion = mesa
				acta.numVotos = 0
				acta.save()


	return HttpResponse("Llamada")


def limpiaActasSanJuan(request):
	# Eliminamos todos los APoliticaUbigeo y Actas asociadas a San Juan de Cutervo y San Juan de Cajamarca
	apus = APoliticaUbigeo.objects.filter(
		Q(ambito_id = 5),
		Q(ubigeo_id = 71) | Q(ubigeo_id = 14)
	)

	apus.delete()

	return HttpResponse("Apus, Actas limpiadas")


def cargaAPoliticasUbigeoSanJuan(request):
	ambito = Ambito.objects.get(pk = 5);
	ubigeoCutervo = Ubigeo.objects.get(pk = 71) #San Juan de Cutervo
	ubigeoCajamarca = Ubigeo.objects.get(pk = 14) #San Juan de Cutervo

	aPoliticasCutervo = AgrupacionPolitica.objects.filter(
		Q(pk = 28) | Q(pk = 29) | Q(pk = 34) | Q(pk = 35) | Q(pk = 36) | Q(pk = 37)
		)

	for ap in aPoliticasCutervo:
		apu = APoliticaUbigeo()
		apu.ubigeo = ubigeoCutervo
		apu.agrupacionPolitica = ap
		apu.ambito = ambito
		apu.save()
		

	aPoliticasCajamarca = AgrupacionPolitica.objects.filter(
		Q(pk = 14) | Q(pk = 9) | Q(pk = 34) | Q(pk = 18) | Q(pk = 32) | Q(pk = 12) | Q(pk = 30) | Q(pk = 26) | Q(pk = 13) | Q(pk = 35) | Q(pk = 36) | Q(pk = 37)
		)

	for ap in aPoliticasCajamarca:
		apu = APoliticaUbigeo()
		apu.ubigeo = ubigeoCajamarca
		apu.agrupacionPolitica = ap
		apu.ambito = ambito
		apu.save()
		

	cargarActasSanJuan()

	return HttpResponse("Data cargada correctamente")


def cargarActasSanJuan():
	# gruposVotacion = GrupoVotacion.objects.all()
	# apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 1) | Q(ambito_id = 2) | Q(ambito_id = 5))
	apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 5), Q(ubigeo_id = 71) | Q(ubigeo_id = 14))
	# apus = APoliticaUbigeo.objects.filter()
	
	for apu in apus:
		ubigeo = apu.ubigeo
		locales = ubigeo.centrovotacion_set.all()
		for local in locales:
			mesas = local.grupovotacion_set.all()
			for mesa in mesas:
				acta = Acta()
				acta.APoliticaUbigeo = apu
				acta.grupoVotacion = mesa
				acta.numVotos = 0
				acta.save()


	return HttpResponse("Cargadas Actas")



	

	



