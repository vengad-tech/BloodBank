
$(document).ready(function(){
$("#inputCity").change(function()
{
	
	$("#load_location").val("yes");
	console.debug("val is "+$("#load_location").val())
	$("#search_form").submit();
}
);
});


$(document).ready(function(){
$("#inputCityProf").change(function()
{
	
	$("#load_location").val("yes");
	console.debug("val is "+$("#load_location").val())
	$("#profile_form").reset();
}
);
});
