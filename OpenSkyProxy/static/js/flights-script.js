//Overriding bootstrap fonts
$(document).ready(function(){
	$("div").css("font-family",'"Helvetica", sans-serif');
})

window.addEventListener('load', function load(){
	//Init map
	// var center = [52.332638, 18.985122];
	// let map = new L.Map('route_map').setView(center, 5);
	// L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png').addTo(map);
	
	// var drawnItems = new L.FeatureGroup();
	// map.addLayer(drawnItems);
	
	// document.getElementById("result").style.display = "none";
	// document.getElementById("route_map").style.display = "none";
	
	document.getElementById("submit_lookup_flights").onclick = function(){
		// Constructing JSON		
		const data = {  
			'id': document.getElementById("id").value,
			'dep_country': document.getElementById("dep_country").value,
			'dep_city': document.getElementById("dep_city").value,
			'dep_airport': document.getElementById("dep_airport").value,
			'dep_time': document.getElementById("dep_time").value,	
			'arr_country': document.getElementById("arr_country").value,
			'arr_city': document.getElementById("arr_city").value,
			'arr_time': document.getElementById("arr_time").value,
			'arr_airport': document.getElementById("arr_airport").value,
			'alt_country': document.getElementById("alt_country").value,	
			'alt_city': document.getElementById("alt_city").value,
			'alt_airport': document.getElementById("alt_airport").value,			
			'plane': document.getElementById("plane").value,
		};
		console.log(data);
		fetch('http://127.0.0.1:8000/lookup-flights/', {
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
			var table = document.getElementById("display_flights_table")
			
			while (table.firstChild) {
				table.removeChild(table.firstChild);
			}
			
			var table_header = document.createElement("thead");
			var header_row = document.createElement("tr");
			var header_id  = document.createElement("th");
			var header_departure  = document.createElement("th");
			var header_arrival  = document.createElement("th");
			var header_alternative  = document.createElement("th");
			var header_plane  = document.createElement("th");
			var header_route  = document.createElement("th");
			
			header_id.innerHTML = "FLIGHT ID";
			header_departure.innerHTML = "DEPARTURE";
			header_arrival.innerHTML = "ARRIVAL";
			header_alternative.innerHTML = "ALTERNATIVE";
			header_plane.innerHTML = "PLANE";
			header_route.innerHTML = "ROUTE";
			
			header_row.appendChild(header_id);
			header_row.appendChild(header_departure);
			header_row.appendChild(header_arrival);
			header_row.appendChild(header_alternative);
			header_row.appendChild(header_plane);
			header_row.appendChild(header_route);
			table_header.appendChild(header_row);
			table.appendChild(table_header);
			
			var table_body = document.createElement("tbody");
			
			json_data.forEach(function(item) {
				var row = document.createElement("tr");
				
				var id  = document.createElement("td");
				var departure  = document.createElement("td");
				var arrival  = document.createElement("td");
				var alternative  = document.createElement("td");
				var plane = document.createElement("td");
				var route = document.createElement("td");
				
				id.innerHTML = item['pk'];
				
				dep_time = item['fields']['departure_time'].split('T');
				departure.innerHTML = item['fields']['departure_airport'] + '\n' + dep_time[0] + ' ' + dep_time[1];
				
				arr_time = item['fields']['arrival_time'].split('T');
				arrival.innerHTML = item['fields']['arrival_airport'] + '\n' + arr_time[0] + ' ' + arr_time[1];
				
				alternative.innerHTML = item['fields']['alternative_airport'];
				
				plane.innerHTML = item['fields']['plane'];
				
				route.innerHTML = item['fields']['route'];
				
				// console.log(item['fields']['route']);
				// item['fields']['route'].forEach(function(point) {
					// route.innerHTML += point + '\n';
				// })
				
				row.appendChild(id);
				row.appendChild(departure);
				row.appendChild(arrival);
				row.appendChild(alternative);
				row.appendChild(plane);
				row.appendChild(route);
				
				table_body.appendChild(row);
			})
			table.appendChild(table_body);
		
			document.getElementById("display_flights_form").style.display = "flex";
		})
		.catch((error) => {
		  console.error('Error:', error);
		});
	};	
	
});
