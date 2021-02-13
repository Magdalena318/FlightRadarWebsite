//Overriding bootstrap fonts
$(document).ready(function(){
	$("div").css("font-family",'"Helvetica", sans-serif');
})

window.onload = function load(){
	//Init map
	var center = [52.332638, 18.985122];
	let map = new L.Map('airports_map', {
	  selectArea: true,
	  attribution: 'PRESS CTRL AND SELECT AREA WITH YOUR MOUSE'
	}).setView(center, 5);
	L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png').addTo(map);
	
	var drawnItems = new L.FeatureGroup();
	map.addLayer(drawnItems);
	var bounds = [['', ''],['', '']];

	
	map.on('areaselected', (e) => {
		drawnItems.clearLayers();
		bounds = [[e.bounds._northEast.lat, e.bounds._northEast.lng], [e.bounds._southWest.lat, e.bounds._southWest.lng]];
		console.log(bounds);
		L.rectangle(bounds, {color: "#262626", weight: 2}).addTo(drawnItems);
	});
	
	
	var select_country = document.getElementById("country");
	select_country.onchange = function(){
		fetch('http://127.0.0.1:8000/lookup-airports?country='+select_country.value, {
			method: 'GET',
		})
		.then(response => response.json())
		.then(data => {
			let json_data = JSON.parse(data);
			var select_city = document.getElementById("city");
			json_data.forEach(function(item) {
				var city = document.createElement("option");
				city.innerHTML = item;
				select_city.appendChild(city);
			})
		})
		.catch((error) => {
		  console.error('Error:', error);
		});
	}
		
	document.getElementById("submit_lookup_airports").onclick = function(){
		// Constructing JSON		
		const data = {  
			"id": document.getElementById("id").value,
			"name": document.getElementById("name").value,
			'country': document.getElementById("country").value,
			'city': document.getElementById("city").value,
			'max_lat': bounds[0][0],
			'min_lat': bounds[1][0],
			'max_lng': bounds[0][1],
			'min_lng': bounds[1][1],
		};
		
		console.log(data);
		
		fetch('http://127.0.0.1:8000/lookup-airports/', {
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
			var table = document.getElementById("display_airports_table")
			
			while (table.firstChild) {
				table.removeChild(table.firstChild);
			}
			
			var table_header = document.createElement("thead");
			var header_row = document.createElement("tr");
			var header_id  = document.createElement("th");
			var header_name  = document.createElement("th");
			var header_country  = document.createElement("th");
			var header_city  = document.createElement("th");
			var header_location  = document.createElement("th");
			
			header_id.innerHTML = "IATA CODE";
			header_name.innerHTML = "NAME";
			header_country.innerHTML = "COUNTRY";
			header_city.innerHTML = "CITY";
			header_location.innerHTML = "LOCATION";
			
			header_row.appendChild(header_id);
			header_row.appendChild(header_name);
			header_row.appendChild(header_country);
			header_row.appendChild(header_city);
			header_row.appendChild(header_location);
			table_header.appendChild(header_row);
			table.appendChild(table_header);
			
			var table_body = document.createElement("tbody");
			
			json_data.forEach(function(item) {
				var row = document.createElement("tr");
				
				var id  = document.createElement("td");
				var name  = document.createElement("td");
				var country  = document.createElement("td");
				var city  = document.createElement("td");
				var airport_location  = document.createElement("td");
				
				id.innerHTML = item['pk'];
				name.innerHTML = item['fields']['name'];
				country.innerHTML = item['fields']['country'];
				city.innerHTML = item['fields']['city'];
				var point = item['fields']['location'].split('POINT ')[1];
				airport_location.innerHTML = point.split(' ')[0] + ', ' + point.split(' ')[1];
				
				row.appendChild(id);
				row.appendChild(name);
				row.appendChild(country);
				row.appendChild(city);
				row.appendChild(airport_location);
				
				table_body.appendChild(row);
			})
			table.appendChild(table_body);
		
			document.getElementById("display_airports_form").style.display = "flex";
		})
		.catch((error) => {
		  console.error('Error:', error);
		});
	};
	
}