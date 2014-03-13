$(document).ready(function(){
    	$(".signInBtn").click(function(){
    	window.location.href = "landing.html";
    	alert("why does this only work with an alert?");
    	});
    	$("#confirmer, #passwordBox").keyup(function() {
    		if ($("#confirmer").val() != $("#passwordBox").val()){
    		$(".alert-danger").show();
    		$("#register").attr("disabled","disabled");
    		} else {
    		$(".alert-danger").hide();
    		$("#register").removeAttr("disabled");
    		}
    		});
    	});
    	