$(document).ready(function(){
$("#editButton").click(function(){
	var aboutText = $("#aboutBox").text();
	var nameText = $(".name").text();
	var majorText = $(".major").text();
	$("#submitButton").show();
	$("#cancelButton").show();
	$(".infoBox").prop('contenteditable','true');
	$(".infoBox").css({"backgroundColor":"white", "color":"gray", "padding-right":"5px", "padding-left":"5px", "-webkit-border-radius":"8px","-moz-border-radius":"8px","border-radius":"8px"});
	$(".infoBox").addClass(".well");
	$(this).hide();	
	$("#cancelButton").click(function(){
	//	$(".editFields").toggle();
	//$(".infoBox").toggle();
	$("#aboutBox").text(aboutText);
	$(".name").text(nameText);
	$(".major").text(majorText);
	$("#editButton").show();
	$(this).hide();	
	$("#submitButton").hide();
	$(".infoBox").prop('contenteditable','false');
	$(".infoBox").css({"backgroundColor":"#F5F5F5", "color":"inherit", "padding-right":"0px", "padding-left":"0px", "-webkit-border-radius":"8px","-moz-border-radius":"8px","border-radius":"8px"});

});
	$("#submitButton").click(function(){
	$("#editButton").show();
	$(this).hide();	
	$("#cancelButton").hide();
	var newName = $('.name').text();
	var newAbout = $('#aboutBox').text();
	var newMajor = $(".major").text();
	var defMajor = "major/department";
	var defAbout = "About me..."
	if (newName == ""){
		$(".name").text(nameText);
	}
	if (newMajor == ""){
		$(".major").text(defMajor);
	}
	if (newAbout == ""){
	$("#aboutBox").text(defAbout);
	}
	
	$(".infoBox").prop('contenteditable','false');
	$(".infoBox").css({"backgroundColor":"#F5F5F5", "color":"inherit", "padding-right":"0px", "padding-left":"0px", "-webkit-border-radius":"8px","-moz-border-radius":"8px","border-radius":"8px"});
	});
});

});