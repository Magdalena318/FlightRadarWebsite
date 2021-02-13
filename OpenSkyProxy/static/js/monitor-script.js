window.onload = function load(){
	// Monitoring
	var center = [52.332638, 18.985122];
	var map = L.map('map').setView(center, 6);
	L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png').addTo(map);
	
	var plane_icon = L.icon({
		iconUrl: PLANE_IMG,
	
		iconSize:     [50, 50], // size of the icon
		iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
		popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
	});
	
	var realtime = L.realtime(`http://127.0.0.1:8000/planes_data?lamin=${map.getBounds()._southWest.lat}&lamax=${map.getBounds()._northEast.lat}&lomin=${map.getBounds()._southWest.lng}&lomax=${map.getBounds()._northEast.lng}`, {
		interval: 10 * 1000,
		getFeatureId: function(feature) {
			return feature.id;
		},
		pointToLayer: function(feature, latlng) {
			var marker = L.marker(latlng, {
				riseOnHover: true,
				icon: plane_icon
			});
			return marker;
		}
	}).addTo(map);
	
	var fetch_address = 'http://127.0.0.1:8000/planes_data?';
	map.on('moveend', function(e) {
	   var lamin = map.getBounds()._southWest.lat;
	   var lamax = map.getBounds()._northEast.lat;
	   var lomin = map.getBounds()._southWest.lng;
	   var lomax = map.getBounds()._northEast.lng;
	   var new_address = `${fetch_address}lamin=${lamin}&lamax=${lamax}&lomin=${lomin}&lomax=${lomax}`;
	   realtime.setUrl(new_address);
	});
	
	document.getElementById("monitor").onclick = function(){
		HideAll();
		document.getElementById("map").style.display = "block";
		map.invalidateSize();
		realtime.start()
	}
}