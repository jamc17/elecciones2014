$(document).ready(function () {
	function numerosPositivos () {
		$("input[name=numVotos]").keydown(function (event) {
            if (event.shiftKey) {
                event.preventDefault();
            }

            if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 13) {
            	if (event.keyCode == 13) {
            		cambiaCampoEnter(event, $(this))
            	}
            }
            else {
                if (event.keyCode < 95) {
                    if (event.keyCode < 48 || event.keyCode > 57) {
                        event.preventDefault();
                    }
                }
                else {
                    if (event.keyCode < 96 || event.keyCode > 105) {
                        event.preventDefault();
                    }
                }
            }
        });
	}

	function cambiaCampoEnter(event, campo) {
		// cb = parseInt(campo.attr("tabindex"));
		// if ($(":input[tabindex=\'" + (cb + 1) + "\']" ) != null) {
		// 	$(":input[tabindex=\'" + (cb + 1) + "\']" ).focus();
		// 	$(":input[tabindex=\'" + (cb + 1) + "\']" ).select();
		// }
		
		var next = campo.parent().next().children()
		if (next[0]){
			next.focus();
			next.select()
			
		} else {
			childs = campo.parent().parent().next().children();
			for (i = 0; i < childs.length; i++) {
				next = $(childs[i]).children();
				if (next[0]) {
					$(next[0]).focus();
					break;
				} 
			} 
		}
		event.preventDefault();
	}
	
	function limpiaListas() {
		$("#provincia").val(0);
		$("#distrito").html("<option value='0'>-- Seleccione Distrito --</option>");
		$("#centroVotacion").html("<option value='0'>-- Local Votación --</option>");
	}

	function limpiaContenido() {
		$("#contenido").html("<h4>Seleccione su local de votación y presione el botón Buscar</h4>");
	}

	function getDistritos(){
		limpiaContenido();
		var ambito = $("#ambito").val();

		var provincia = $(this).val();
		if (provincia == 0) {
			limpiaListas();
			return ;
		}

		$("#distrito").load("distritos/"+provincia+"/" + ambito, function () {
			getLocalesVotacion();
		})
	}

	function getLocalesVotacion(e){
		limpiaContenido();

		var form = $("#formSelUbigeo");
		var params = $(form).serialize();

		$("#centroVotacion").load("/?" + params);
	}

	function getResumenCentroVotacion(e){
		e.preventDefault();
		var ambito = $("#ambito").val();
		var cv = $("#centroVotacion").val();
		var url = "getResumenCentroVotacion/" + cv +"/"  + ambito;
		
		$("#resumenCentroVotacion").load(url, function () {

		})
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
			$("#btnResumenCentroVotacion").on("click", getResumenCentroVotacion)
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
			$("#resetActa").on("click", resetActa);
			numerosPositivos();
			configuraActaDistrital();
		});
	}

	function configuraActaDistrital() {
		var ambito = $("#ambito").val();
		if (ambito == "5") {
			//Configuramos el orden de los campos
			var inputsVotos = $("input[data-ambito='Municipal Distrital']");
			for (i = 0; i<inputsVotos.length; i++) {
				var input = $(inputsVotos[i]);
				var parent = input.parent()
				nodePrev = parent.prev().children()[0];
				console.log($(nodePrev));
				if (nodePrev == undefined) {
					input.detach();
					parent.append(input);
				}
			}
		}
	}

	function resetActa(e) {
		e.preventDefault();

		var res = confirm("Está Seguro que desea resetear el acta?");
		
		if (res) {
			var inputs = $("input[name=numVotos]");
			inputs.val(0);
			registrarActa(e);
		} 
		
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
		var action = "registrar";

		var node = $(e.target).attr("id")

		if (node == "resetActa") {
			action = "resetActa";
		}

		var electoresHabiles = $("#electores").html();
		var votosEmitidos = $("input[data-partido=38]");		

		if (votosEmitidos.length == 2) {
			if ($(votosEmitidos[0]).val() !== $(votosEmitidos[1]).val()) {
				var c = confirm("Total de votos emitidos no coinciden, desea continuar");
				if (!c) {
					return;
				}
			}
		}

		if ($(votosEmitidos[0]).val() > electoresHabiles) {
			var ct = confirm("El total de votos emitidos es mayor que los electores habiles, desea continuar?");
			if (!ct) {
				return;
			}
		}


		$.ajax({
	        url: 'registrarActaSubmit/',
	        type: 'POST',
	        data: {json: JSON.stringify(formJson), csrfmiddlewaretoken: csfrtoken, centroVotacion: centroVotacion, grupoVotacion: grupoVotacion, action: action},
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
	$("#ambito").on("change", limpiaListas);
	$("#provincia").on("change", getDistritos);
	$("#distrito").on("change", getLocalesVotacion);
});