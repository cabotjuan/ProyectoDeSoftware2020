$(document).ready(function () {
    let latitud = $("#mapaFijo").data('lat')
    let longitud = $("#mapaFijo").data('lon')
    let info = $("#mapaFijo").data('info')

    var nuevoMapa = L.map('mapaFijo').setView([latitud, longitud], 13)
    console.log(nuevoMapa)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(nuevoMapa);

    marker = L.marker([latitud, longitud]).addTo(nuevoMapa).bindPopup(info).openPopup();
});