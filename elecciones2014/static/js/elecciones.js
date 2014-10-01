$(document).ready(function () {
	function getDistritos(){
		$("#distrito").load("distritos/"+$(this).val())
	}

	function getLocalesVotacion(e){
		e.preventDefault();
		var params = $(this).serialize();

		$("#centrosVotacion").load("/?" + params, function () {
			$(".centroVotacion").on("click", getGruposVotacion);
		});

	}

	function getGruposVotacion(e){
		e.preventDefault();
		var url = $(this).attr("href");
		$("#centrosVotacion").load(url, function () {
			$(".grupoVotacion").on("click", getActa);
		});
	}

	function getActa(e){
		e.preventDefault();
		var url = $(this).attr("href");
		var distrito = $("#distrito").val();
		var ambito = $("#ambito").val();
		url += "/" + distrito + "/" + ambito;
		$("#centrosVotacion").load(url, function () {
			$("#formRegistrarActa").on("submit", registrarActa)
		});
	}

	function registrarActa(e){
		e.preventDefault();
		var inputs = $("input[name=numVotos]");
		var formJson = [];

		inputs.each(function (index) {
			formJson.push({"actaId": $(this).attr("data-acta"), "numVotos": $(this).val()});
		})

		var csfrtoken = $("input[name=csrfmiddlewaretoken]").val();

		$.ajax({
	        url: 'registrarActaSubmit/',
	        type: 'POST',
	        data: {json: JSON.stringify(formJson), csrfmiddlewaretoken: csfrtoken},
	        dataType: 'json',
	        success: function (data, textStatus, jqXHR) {
	        	
	        }
	    });
	}


	$("#formSelUbigeo").on("submit", getLocalesVotacion);
	$("#provincia").on("change", getDistritos);
});