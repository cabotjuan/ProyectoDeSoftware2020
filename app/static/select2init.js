$(document).ready(function () {
    $('#municipios').select2();
    $('#municipios').append('<option disabled selected value style="display:none;">Elegí un municipio...</option>');
    $('#tiposcentro').select2();
    $('#tiposcentro').append('<option disabled selected value style="display:none;">Elegí un tipo...</option>');
    $('select2').addClass("w100important");
    console.log('/centros/'+{{ centro.id }} )
    $('#municipios option').each(function (e) {
        
    })





});