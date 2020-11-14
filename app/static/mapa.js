$(document).ready(function () {
    if ($("#latitude").val(), $("#longitude").val())
        var mymap = L.map('mapid').setView([$("#latitude").val(), $("#longitude").val()], 13);
    else
        var mymap = L.map('mapid').setView([-34.9187, -57.956], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mymap);

    mymap.attributionControl.setPrefix(false);
    console.log($("#latitude").val(), $("#longitude").val())
    var marker = L.marker([$("#latitude").val(), $("#longitude").val()], { draggable: 'true' }).addTo(mymap);
    var popup = L.popup();


    function onMapClick(e) {
        marker.setLatLng(e.latlng).addTo(mymap);
        popup
            .setLatLng(e.latlng)
            .setContent("Coordenadas: " + e.latlng.toString());
        marker.bindPopup(popup.getContent()).openPopup();
        $("#latitude").val(e.latlng.lat);
        $("#longitude").val(e.latlng.lng);

    }

    marker.on('dragend', function (e) {
        let position = marker.getLatLng();
        popup
            .setLatLng(position)
            .setContent("Coordenadas: " + position.toString());

        marker.setLatLng(position, {
            draggable: 'true'
        }).bindPopup(popup.getContent()).openPopup();
        $("#latitude").val(position.lat);
        $("#longitude").val(position.lng);

    });

    mymap.on('click', onMapClick);
});