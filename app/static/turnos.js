$(document).ready(function () {

    function cargarTurnosDisponibles(FECHA, C_ID){
        fetch('/administracion/centros/' + C_ID + '/turnos_disponibles?fecha=' + FECHA)
            .then((resp) => resp.json())
            .then((data) => {
                $('#TurnosDisponibles').children().remove()
                $('#TurnosDisponibles').append('<option disabled selected value style="display:none;">Seleccionar...</option>');
                Object.entries(data).forEach(
                    ([key, turnos]) => turnos.forEach(
                        (turno) => {
                            $('#TurnosDisponibles').append('<option value="' + turno.hora_inicio + '">' + turno.hora_inicio + '</option>')
                        }
                    )
                );
            })

        $("#HoraTurno").val($("#TurnosDisponibles").val())
    }

    if (($("#FechaTurno").val() ) && ( $("#FechaTurno").data('centro') != null ) ) {
        var FECHA = $("#FechaTurno").val()
        var C_ID = $("#FechaTurno").data('centro')
        cargarTurnosDisponibles(FECHA, C_ID);
    }
    $('#CentroSelect').append('<option disabled selected value style="display:none;">Seleccionar...</option>');

    
    $("#HoraTurno").val($("#TurnosDisponibles").val())


    $("#CentroSelect").change(function () {

        let C_ID = $("#CentroSelect option:selected").val()
        var FECHA = $("#FechaTurno").val()
        if (FECHA) {
            cargarTurnosDisponibles(FECHA, C_ID);
        }

    });

    $("#FechaTurno").change(function () {
        var FECHA = $("#FechaTurno").val()
        let C_ID = $("#CentroSelect option:selected").val()
        if ( $("#FechaTurno").data('centro') > 0 ){ 
            C_ID = $("#FechaTurno").data('centro')
        }
        cargarTurnosDisponibles(FECHA, C_ID);
    });

    $("#TurnosDisponibles").change(function () {
        $("#HoraTurno").val(this.value)
    });

});
