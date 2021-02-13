//Overriding bootstrap fonts
$(document).ready(function(){
	$("div").css("font-family",'"Helvetica", sans-serif');
})
	
window.addEventListener('load', function load(){
	document.getElementById("result").style.display = "none";
	
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
	
	document.getElementById("submit_flight").onclick = function(){
		// Constructing JSON		
		const data = {  
			'dep_airport': document.getElementById("dep_airport").value,
			'dep_time': document.getElementById("dep_time").value,		
			'arr_airport': document.getElementById("arr_airport").value,
			'alt_airport': document.getElementById("alt_airport").value,			
			'plane': document.getElementById("plane").value,
		};
		
		fetch('http://127.0.0.1:8000/add/', {
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
			console.log(json_data);
			if(json_data.result=='Success'){
				document.getElementById("result").style.display = "block";	
				document.getElementById("result").classList.add("text-success");
				document.getElementById("result").classList.remove("text-danger");				
				document.getElementById("result_text").innerHTML = json_data.reason;
				document.getElementById("flight_id").innerHTML = json_data.id;
			} else if(json_data.result=='Failure'){
				document.getElementById("result").style.display = "block";		
				document.getElementById("result").classList.add("text-danger");
				document.getElementById("result").classList.remove("text-success");
				document.getElementById("result_text").innerHTML = json_data.reason;
				document.getElementById("flight_id_text").style.display = 'none';
			}
		})
		.catch((error) => {
		  console.error('Error:', error);
		});
	};	
});
