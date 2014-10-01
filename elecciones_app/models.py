from django.db import models

class Ambito(models.Model):
	nombre = models.CharField(max_length=35)

	def __unicode__(self):
		return self.nombre


class Ubigeo(models.Model):
	codDep = models.CharField(max_length=2)
	codPro = models.CharField(max_length=2)
	codDis = models.CharField(max_length=2)
	nombre = models.CharField(max_length=70)

	def __unicode__(self):
		return self.nombre


class CentroVotacion(models.Model):
	nombre = models.CharField(max_length=140)
	ubigeo = models.ForeignKey(Ubigeo)

	def __unicode__(self):
		return self.nombre


class GrupoVotacion(models.Model):
	codigo = models.CharField(max_length=8)
	centroVotacion = models.ForeignKey(CentroVotacion)
	electoresHabiles = models.IntegerField(null=True, blank=True)
	contabilizado = models.BooleanField(default = False)

	def __unicode__(self):
		return self.codigo


class AgrupacionPolitica(models.Model):
	nombre = models.CharField(max_length=70)
	logo = models.ImageField(null=True, blank=True)
	ubigeo = models.ManyToManyField(Ubigeo, through = "APoliticaUbigeo")

	def __unicode__(self):
		return self.nombre


class APoliticaUbigeo(models.Model):
	ubigeo = models.ForeignKey(Ubigeo)
	agrupacionPolitica = models.ForeignKey(AgrupacionPolitica)
	ambito = models.ForeignKey(Ambito)

	def __unicode__(self):
		return self.ambito.nombre + " -> " + self.ubigeo.nombre + " -> " + self.agrupacionPolitica.nombre 


class Acta(models.Model):
	APoliticaUbigeo = models.ForeignKey(APoliticaUbigeo)
	grupoVotacion = models.ForeignKey(GrupoVotacion, null=True, blank=True)
	numVotos = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.APoliticaUbigeo.ubigeo.nombre + " -> " + self.grupoVotacion.codigo + " - " + str(self.numVotos)







