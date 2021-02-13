//Overriding bootstrap fonts
$(document).ready(function(){
	$("div").css("font-family",'"Helvetica", sans-serif');
})

window.addEventListener('load', function load(){
	//Init map
	var center = [52.332638, 18.985122];
	let map = new L.Map('route_map').setView(center, 5);
	L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png').addTo(map);
	
	var drawnItems = new L.FeatureGroup();
	map.addLayer(drawnItems);
	
	var redIcon = new L.Icon({
	  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
	  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	  iconSize: [25, 41],
	  iconAnchor: [12, 41],
	  popupAnchor: [1, -34],
	  shadowSize: [41, 41]
	});
	
	document.getElementById("result").style.display = "none";
	document.getElementById("route_map").style.display = "none";
	
	document.getElementById("calculate_route").onclick = function(){
		// Constructing JSON		
		const data = {  
			'dep_airport': document.getElementById("dep_airport").value,
			'dep_time': document.getElementById("dep_time").value,		
			'arr_airport': document.getElementById("arr_airport").value,
			'alt_airport': document.getElementById("alt_airport").value,			
			'plane': document.getElementById("plane").value,
		};
		console.log(data);
		fetch('http://127.0.0.1:8000/route/', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json',
			'X-CSRFTOKEN': Cookies.get('csrftoken'),
			},
			body: JSON.stringify(data)
		})
		.then(response => response.json())
		.then(data => {
			let json_data = JSON.parse(data);

			if(json_data.result=='Success'){
				document.getElementById("result").style.display = "none";	
				document.getElementById("route_map").style.display = "block";
				map.invalidateSize();
				drawnItems.clearLayers();

				var route = new L.Polyline(json_data.route, {
					color: 'red',
					weight: 3,
					opacity: 0.5,
					smoothFactor: 1
				});
				route.addTo(drawnItems);
				
				var count = 0;
				json_data.route.forEach(function(item) {
					if(json_data.waypoints[count].includes('<')){
						var marker = L.marker(item, {icon: redIcon}).bindTooltip(String(item), {permanent: true, direction: 'right'}).addTo(drawnItems);
					} else{
						var tooltip_text = json_data.waypoints[count] + '<br>' + item;
						var marker = L.marker(item, {icon: redIcon}).bindTooltip(tooltip_text, {permanent: true, direction: 'right'}).addTo(drawnItems);
					}
					count++;
				})				
			} else if(json_data.result=='Failure'){
				document.getElementById("result").style.display = "block";		
				document.getElementById("result").classList.remove("text-success");
				document.getElementById("result").classList.add("text-danger");
				document.getElementById("result_text").innerHTML = json_data.reason;
			}
		})
		.catch((error) => {
		  console.error('Error:', error);
		});
	};	
	
});
