function removeOptions(selectElement) {
   var i, L = selectElement.options.length - 1;
   for(i = L; i >= 0; i--) {
      selectElement.remove(i);
   }
}

function optionExists(selectElement, selectValue){
	for (i = 0; i < selectElement.length; ++i){
		if (selectElement.options[i].value == selectValue){
		  return true;
		}
	}
	return false;
}

function onCountryChange(select_country){
	fetch('http://127.0.0.1:8000/responsive-form?country=' + select_country.value, {
		method: 'GET',
	})
	.then(response => response.json())
	.then(data => {
		let json_data = JSON.parse(data);
		
		let select_city = document.getElementById(select_country.id.split('_')[0]+'_city');
		let city_value = select_city.value;

		removeOptions(select_city);
		json_data['cities'].forEach(function(item) {
			var city = document.createElement("option");
			city.innerHTML = item;
			select_city.appendChild(city);
		})
		if (optionExists(select_city, city_value)){			
			select_city.value = city_value;
		}
		
		let select_airport = document.getElementById(select_country.id.split('_')[0]+'_airport');
		let airport_value = select_airport.value;
		removeOptions(select_airport);
		json_data['airports'].forEach(function(item) {
			var airport = document.createElement("option");
			airport.innerHTML = item;
			select_airport.appendChild(airport);
		})
		if (optionExists(select_airport, airport_value)){
			select_airport.value = airport_value;
		}
	})
	.catch((error) => {
	  console.error('Error:', error);
	});
}

function onCityChange(select_city){
	fetch('http://127.0.0.1:8000/responsive-form?city=' + select_city.value, {
		method: 'GET',
	})
	.then(response => response.json())
	.then(data => {
		console.log(data);
		let json_data = JSON.parse(data);
		
		let select_country = document.getElementById(select_city.id.split('_')[0]+'_country');		
		let select_airport = document.getElementById(select_city.id.split('_')[0]+'_airport');
		removeOptions(select_airport);
		
		if(json_data.length==1){
			select_country.value = json_data[0]['country'];
			json_data[0]['airports'].forEach(function(item) {
				var airport = document.createElement("option");
				airport.innerHTML = item;
				select_airport.appendChild(airport);
			})
		} else{
			var max_length = 0;
			var country;
			json_data.forEach(function(item) {
				if(item['airports'].length>max_length){
					max_length=item['airports'].length;
					country=item;
				}
			})

			select_country.value = country['country'];
			country['airports'].forEach(function(item) {
				var airport = document.createElement("option");
				airport.innerHTML = item;
				select_airport.appendChild(airport);
			})
		}
		if (optionExists(select_airport, airport_value)){
			select_airport.value = airport_value;
		}
	})
	.catch((error) => {
	  console.error('Error:', error);
	});
}

function onAirportChange(select_airport){
	fetch('http://127.0.0.1:8000/responsive-form?airport=' + select_airport.value, {
		method: 'GET',
	})
	.then(response => response.json())
	.then(data => {
		console.log(data);
		let json_data = JSON.parse(data);
		
		let select_country = document.getElementById(select_airport.id.split('_')[0]+'_country');
		select_country.value = json_data['country'];
		
		let select_city = document.getElementById(select_airport.id.split('_')[0]+'_city');
		select_city.value = json_data['city'];
	})
	.catch((error) => {
	  console.error('Error:', error);
	});
}