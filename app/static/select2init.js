$(document).ready(function () {
    $('#municipios').select2()
    $('#municipios').select2().val($('#municipios').data('value')).change();
    $('#municipios').append('<option disabled value style="display:none;">Elegí un municipio...</option>');
    $('#tiposcentro').select2()
    $('#tiposcentro').select2().val($('#tiposcentro').data('centro')).change();
    $('#tiposcentro').append('<option disabled value style="display:none;">Elegí un tipo...</option>');
    $('select2').addClass("w100important");
});
