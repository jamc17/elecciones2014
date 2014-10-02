$(document).ready(function () {
	function limpiaContenido() {
		$("#contenido").html("<h4>Seleccione su local de votación y presione el botón Buscar</h4>");
	}

	function getDistritos(){
		limpiaContenido();

		$("#distrito").load("distritos/"+$(this).val(), function () {
			getLocalesVotacion();
		})
	}

	function getLocalesVotacion(e){
		limpiaContenido();

		var form = $("#formSelUbigeo");
		var params = $(form).serialize();

		$("#centroVotacion").load("/?" + params);
	}

	function getGruposVotacion(e){
		if (e) {
			e.preventDefault();	
		}
		
		var centroVotacion = $("#centroVotacion").val()

		if (centroVotacion === '0') {
			alert("Seleccione un centro de votación");
			return;
		}

		var url = "gruposVotacion/" + centroVotacion
		

		$("#contenido").load(url, function () {
			$(".grupoVotacion").on("click", getActa);
		});
	}

	function getActa(e){
		e.preventDefault();
		var url = $(this).attr("href");
		var distrito = $("#distrito").val();
		var ambito = $("#ambito").val();
		url += "/" + distrito + "/" + ambito;
		$("#contenido").load(url, function () {
			$("#formRegistrarActa").on("submit", registrarActa);
			$("#resetForm").on("click", getGruposVotacion);
		});
	}

	function registrarActa(e){
		e.preventDefault();
		var inputs = $("input[name=numVotos]");
		var formJson = [];

		inputs.each(function (index) {
			if ($(this).val() == '') {
				$(this).val(0);
			}
			formJson.push({"actaId": $(this).attr("data-acta"), "numVotos": $(this).val()});
		})
		var csfrtoken = $("input[name=csrfmiddlewaretoken]").val();
		var centroVotacion = $("#centroVotacion").val();
		var grupoVotacion = $("#grupoVotacion").val();

		$.ajax({
	        url: 'registrarActaSubmit/',
	        type: 'POST',
	        data: {json: JSON.stringify(formJson), csrfmiddlewaretoken: csfrtoken, centroVotacion: centroVotacion, grupoVotacion: grupoVotacion},
	        dataType: 'json',
	        success: function (data, textStatus, jqXHR) {
	        	if (data.estado == 1) {
					getGruposVotacion();
	        	}
	        	else{
	        		alert("Error: No se puedo guardar el acta...")
	        	}
	        }
	    });
	}


	$("#formSelUbigeo").on("submit", getGruposVotacion);
	$("#ambito").on("change", limpiaContenido);
	$("#provincia").on("change", getDistritos);
	$("#distrito").on("change", getLocalesVotacion);
});