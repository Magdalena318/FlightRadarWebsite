//Overriding bootstrap fonts
$(document).ready(function(){
	$("div").css("font-family",'"Helvetica", sans-serif');
})

window.onload = function load(){
	document.getElementById("display_airplanes_form").style.display = "none";
	document.getElementById("lookup_airplanes_form").style.display = "flex";

	document.getElementById("submit_lookup_airplanes").onclick = function(){
		// Constructing JSON		
		const data = {  
			"name": document.getElementById("name").value,
			'max_flight_range': flight_range_slider.getValue().maxValue.toString(),
			'min_flight_range': flight_range_slider.getValue().minValue.toString(),
			'max_speed_range': speed_range_slider.getValue().maxValue.toString(),
			'min_speed_range': speed_range_slider.getValue().minValue.toString(),
			'max_passenger_max': max_passenger_slider.getValue().maxValue.toString(),
			'max_passenger_min': max_passenger_slider.getValue().minValue.toString(),
		};
		
		console.log(JSON.stringify(data));
		console.log(Cookies.get('sessionid'));
		
		fetch('http://127.0.0.1:8000/lookup-airplanes/', {
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
			var table = document.getElementById("display_airplanes_table")
			
			var table_header = document.createElement("thead");
			var header_row = document.createElement("tr");
			var header_name  = document.createElement("th");
			var header_frange  = document.createElement("th");
			var header_speed  = document.createElement("th");
			var header_maxp  = document.createElement("th");
			
			header_name.innerHTML = "NAME";
			header_frange.innerHTML = "FLIGHT RANGE";
			header_speed.innerHTML = "CRUISE SPEED";
			header_maxp.innerHTML = "MAXIMUM PASSENGERS";
			
			header_row.appendChild(header_name);
			header_row.appendChild(header_frange);
			header_row.appendChild(header_speed);
			header_row.appendChild(header_maxp);
			table_header.appendChild(header_row);
			table.appendChild(table_header);
			
			var table_body = document.createElement("tbody");
			
			json_data.forEach(function(item) {
				var row = document.createElement("tr");
				
				var name  = document.createElement("td");
				var flight_range  = document.createElement("td");
				var speed  = document.createElement("td");
				var max_passenger  = document.createElement("td");
				
				name.innerHTML = item['pk'];
				flight_range.innerHTML = item['fields']['flight_range'];
				speed.innerHTML = item['fields']['speed'];
				max_passenger.innerHTML = item['fields']['max_passenger'];
				
				row.appendChild(name);
				row.appendChild(flight_range);
				row.appendChild(speed);
				row.appendChild(max_passenger);
				
				table_body.appendChild(row);
			})
			table.appendChild(table_body);
		
			document.getElementById("display_airplanes_form").style.display = "flex";
		})
		.catch((error) => {
		  console.error('Error:', error);
		});
	};
}