from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.db.models import Q, Sum
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import json
from .models import Ambito, Ubigeo, CentroVotacion, GrupoVotacion, AgrupacionPolitica, APoliticaUbigeo, Acta



def viewLogin(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('home'))

			else:
				#Return a 'Disable account' error message
				return HttpResponse('El usuario que esta ingresando esta inactivo')
		else:
			# Return a 'invalid login' error message
			msg = {'error_message' : 'Usuario y/o password incorrectos'}
			return render(request, 'elecciones_app/login.html', msg)

	if not request.user.is_authenticated():
		return render(request, 'elecciones_app/login.html', locals())
	else:
		return HttpResponseRedirect(reverse('home'))


@login_required
def viewLogout(request):
	logout(request)
	return redirect(reverse('viewLogin'))


def getPermisos(request, provincias):
	user = request.user.username
	if user == "odpsanpablo":
		provincias = provincias.filter(Q(pk = 111) | Q(pk = 125) | Q(pk = 53))

	elif user == "odphualgayoc":
		provincias = provincias.filter(Q(pk = 78))

	elif user == "odpcutervo":
		provincias = provincias.filter(Q(pk = 62))

	elif user == "odpchota":
		provincias = provincias.filter(Q(pk = 33) | Q(pk = 130))

	elif user == "odpjaen":
		provincias = provincias.filter(Q(pk = 82) | Q(pk = 95))

	elif user == "odpcajamarca":
		provincias = provincias.filter(Q(pk = 15) | Q(pk = 20) | Q(pk = 2) | Q(pk = 103))

	return provincias
	

@login_required
def index(request):
	ambitos = Ambito.objects.all().exclude(Q(pk = 1) | Q(pk = 2) | Q(pk = 6)).order_by("pk")
	regiones = Ubigeo.objects.filter(codDep = '06', codPro = '00', codDis="00")
	provincias = Ubigeo.objects.filter(codDep = "06", codDis = "00").exclude(codPro = '00').order_by("nombre")

	provincias = getPermisos(request, provincias)



	if (request.GET.get("ambito") and request.GET.get("provincia") and request.GET.get("distrito")) :
		distrito = Ubigeo.objects.get(pk = request.GET.get("distrito"))
		centrosVotacion = CentroVotacion.objects.filter(ubigeo = distrito).order_by("nombre")
		return render(request, "elecciones_app/centrosVotacion.html", locals())
	

	else:
		return render(request, "elecciones_app/index.html", locals())

def gruposVotacion(request, idCentroVotacion, idAmbito, idUbigeo):
	centroVotacion = CentroVotacion.objects.get(pk = idCentroVotacion)
	ambito = Ambito.objects.get(pk = idAmbito)
	ubigeo = Ubigeo.objects.get(pk = idUbigeo)
	if ambito.nombre == "Regional":
		apus = APoliticaUbigeo.objects.filter(ubigeo = ubigeo, ambito_id = 1)
	else:
		apus = APoliticaUbigeo.objects.filter(ubigeo = ubigeo, ambito = ambito)
	
	apu = apus[0]
	# grupoVotacionActas = GrupoVotacion.acta_set.filter(APoliticaUbigeo = apu)
	actasGV =  apu.acta_set.all();
	gruposVotacion = GrupoVotacion.objects.filter(centroVotacion = centroVotacion).order_by("codigo")
	totalElectores = gruposVotacion.aggregate(cantidad = Sum('electoresHabiles'))

	return render(request, "elecciones_app/gruposVotacion.html", locals())


def getResumenCentroVotacion(request, idCentroVotacion, idAmbito):
	centroVotacion = CentroVotacion.objects.get(pk = idCentroVotacion)
	ubigeo = centroVotacion.ubigeo
	ambito = Ambito.objects.get(pk = idAmbito)
	
	if ambito.nombre == "Regional":
		# apus = ubigeo.apoliticaubigeo_set.filter(Q(ambito__pk = 1)| Q(ambito__pk = 2))
		apus = APoliticaUbigeo.objects.filter(ubigeo = ubigeo, ambito__pk = 1).filter(acta__grupoVotacion__centroVotacion = centroVotacion).annotate(numVotos = Sum("acta__numVotos"))

		apusCons = APoliticaUbigeo.objects.filter(ubigeo = ubigeo, ambito__pk = 2).filter(acta__grupoVotacion__centroVotacion = centroVotacion).annotate(numVotos = Sum("acta__numVotos"))

	else:
		# apus = ubigeo.apoliticaubigeo_set.filter(Q(ambito__pk = 1)| Q(ambito__pk = 2))
		apus = APoliticaUbigeo.objects.filter(Q(ubigeo = ubigeo), Q(ambito = ambito)).filter(acta__grupoVotacion__centroVotacion = centroVotacion).annotate(numVotos = Sum("acta__numVotos"))

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
			acta.estado = 1
			
			if action == "resetActa":
				acta.estado = 0
			
			acta.save()

		# grupoVotacion = GrupoVotacion.objects.get(pk = grupoVotacionId)
		# grupoVotacion.contabilizado = True
		# if action == "resetActa":
		# 	grupoVotacion.contabilizado = False
		
		# grupoVotacion.save()

		response_data['estado'] = 1
		response_data['message'] = "Datos guardados correctamente"
		
	except Exception, e:
		response_data['estado'] = 0
		response_data['message'] = "Error: " + str(e)

	return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required
def reportes(request):
	ambitos = Ambito.objects.all().exclude(Q(pk = 3) | Q(pk = 6)).order_by("pk")
	regiones = Ubigeo.objects.filter(codDep = '06', codPro = '00', codDis="00")
	provincias = Ubigeo.objects.filter(codDep = "06", codDis = "00").exclude(codPro = '00').order_by("nombre")

	provincias = getPermisos(request, provincias)


	if (request.GET.get("ambito") and request.GET.get("provincia") and request.GET.get("distrito")) :
		distrito = Ubigeo.objects.get(pk = request.GET.get("distrito"))
		centrosVotacion = CentroVotacion.objects.filter(ubigeo = distrito).order_by("nombre")
		return render(request, "elecciones_app/centrosVotacion.html", locals())
	

	else:
		return render(request, "elecciones_app/reportes.html", locals())

def getReporteUbigeo(request, idAmbito, idProvincia = 0, idDistrito = 0):
	# centroVotacion = CentroVotacion.objects.get(pk = idCentroVotacion)
	# distrito = Ubigeo.objects.get(pk = idDistrito)
	ambito = Ambito.objects.get(pk = idAmbito)

	aPoliticas = AgrupacionPolitica.objects.filter(apoliticaubigeo__ambito = ambito).annotate(numVotos = Sum("apoliticaubigeo__acta__numVotos"))

	template = "elecciones_app/reportesRegional.html"

	if idProvincia != "0":
		ubigeo = Ubigeo.objects.get(pk = idProvincia)
		aPoliticas = AgrupacionPolitica.objects.filter(apoliticaubigeo__ambito = ambito, apoliticaubigeo__ubigeo__codPro = ubigeo.codPro).annotate(numVotos = Sum("apoliticaubigeo__acta__numVotos"))
		template = "elecciones_app/reportesRegional.html"
		

	if idDistrito != "0":
		ubigeo = Ubigeo.objects.get(pk = idDistrito)
		apus = APoliticaUbigeo.objects.filter(ubigeo = ubigeo, ambito = ambito).annotate(numVotos = Sum("acta__numVotos"))
		template = "elecciones_app/reportesDistrito.html"

	return render(request, template, locals())


@login_required
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


@login_required
def cargarActas(request):
	# gruposVotacion = GrupoVotacion.objects.all()
	apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 1) | Q(ambito_id = 2) | Q(ambito_id = 4) | Q(ambito_id = 5))
	# apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 4))
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


@login_required
def limpiaActasSanJuan(request):
	# Eliminamos todos los APoliticaUbigeo y Actas asociadas a San Juan de Cutervo y San Juan de Cajamarca
	apus = APoliticaUbigeo.objects.filter(
		Q(ambito_id = 5),
		Q(ubigeo_id = 71) | Q(ubigeo_id = 14)
	)

	apus.delete()

	return HttpResponse("Apus, Actas limpiadas")


@login_required
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


@login_required
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


def limpiaTotalesMunicipales(request):
	apus = APoliticaUbigeo.objects.filter(Q(agrupacionPolitica__pk = 38), Q(ambito_id = 5)| Q(ambito_id = 4))
	apus.delete()
	return HttpResponse("Delete")


@login_required
def cargaTotalesMunicipales(request):
	# apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 4) | Q(ambito_id = 5))
	ap = AgrupacionPolitica.objects.get(pk = 38)
	ubigeos = Ubigeo.objects.exclude(codDis = "00")
	ambitos = Ambito.objects.filter(
		Q(pk = 4) | Q(pk = 5)
		)

	try:
		for ambito in ambitos:
			for ubigeo in ubigeos:
				apu = APoliticaUbigeo()
				apu.ubigeo = ubigeo
				apu.agrupacionPolitica = ap
				apu.ambito = ambito
				apu.save()

		return HttpResponse("Total Votos Emitidos cargados correctamente")

	except Exception, e:
		raise e


@login_required
def cargaActasTotalesMunicipales(request):
	apus = APoliticaUbigeo.objects.filter(Q(ambito_id = 4) | Q(ambito_id = 5), Q(agrupacionPolitica_id = 38))

	try:
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

	except Exception, e:
		raise e




@login_required
def configuraDistritosCapitales(request):
	distritos = Ubigeo.objects.filter(Q(pk = 3) | Q(pk = 16) | Q(pk = 21) |Q(pk = 34) |Q(pk = 54) |Q(pk = 63) |Q(pk = 79) | Q(pk = 83) | Q(pk = 96) | Q(pk = 104) | Q(pk = 112) | Q(pk = 126) | Q(pk = 131))

	for distrito in distritos:
		distrito.distritoCapital = True
		distrito.save()

	return HttpResponse("Configurados distritos capitales")


@login_required
def resetDatabaseEleccionesRM(request):
	actas = Acta.objects.all()
	for acta in actas:
		acta.numVotos = 0
		acta.save()

	return HttpResponse("Datos limpiados correctamente")


def prueba(request):
	acta = Acta.objects.get(pk = 1)
	HttpResponse(acta.numVotos + " - " + acta.pk + " - " + acta.estado)






	

	



