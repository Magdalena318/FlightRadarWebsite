window.addEventListener('load', function load(){
	document.getElementById("dep_country").value = 'Poland';
	document.getElementById("arr_country").value = 'United Kingdom'; 
	document.getElementById("alt_country").value = 'Ireland';
	
	document.getElementById("dep_city").value = 'Warsaw'; 
	document.getElementById("arr_city").value = 'London'; 
	document.getElementById("alt_city").value = 'Dublin';
	
	document.getElementById("dep_airport").value = 'Warsaw Chopin Airport'; 
	document.getElementById("arr_airport").value = 'London Heathrow Airport'; 
	document.getElementById("alt_airport").value = 'Dublin Airport';
	
	//Automatically set the dep_time to the current local time
	var current_date = new Date().toLocaleString("sv-SE", {
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
		hour: "2-digit",
		minute: "2-digit",
		second: "2-digit"
	}).replace(" ", "T");
	$("#dep_time").val(current_date);
});

