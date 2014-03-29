$(document).ready(function(){
$("#editButton").click(function(){
	$(".projPic").click(function(){
	$(".picChange").trigger("click");
	});
	var aboutText = $("#descriptionBox").text();
	var nameText = $(".name").text();
	$(".name").keyup(function(){
	var checkName = $(".name").text();
	checkName = $.trim(checkName);
	if (checkName == ""){
	$(".name").text(nameText);
	}
	});
	$("#submitButton").show();
	$("#cancelButton").show();
	$(".infoBox").prop('contenteditable','true');
	$(".infoBox").css({"backgroundColor":"white", "color":"gray", "padding-right":"5px", "padding-left":"5px", "-webkit-border-radius":"8px","-moz-border-radius":"8px","border-radius":"8px"});
	$(".infoBox").addClass(".well");
	$(this).hide();	
	$("#favoriteButton").hide();
	$("#applyButton").hide();
	$("#cancelButton").click(function(){
	// NEW
	$(".projPic").unbind();

	$("#descriptionBox").text(aboutText);
	$(".name").text(nameText);
	$("#editButton").show();
	$(this).hide();	
	$("#submitButton").hide();
	$("#applyButton").show();
	$("#favoriteButton").show();
	$(".infoBox").prop('contenteditable','false');
	$(".infoBox").css({"backgroundColor":"#F5F5F5", "color":"inherit", "padding-right":"0px", "padding-left":"0px", "-webkit-border-radius":"8px","-moz-border-radius":"8px","border-radius":"8px"});

	});
	$("#submitButton").click(function(){
	$(".projPic").unbind();
	$("#editButton").show();
	$(this).hide();	
	$("#cancelButton").hide();
	$("#applyButton").show();
	$("#favoriteButton").show();
	var newName = $('.name').text();
	var newDescription = $('#descriptionBox').text();
	var defDescription = "Description..."
	if (newName == ""){
		$(".name").text(nameText);
	} else {
		$(".name").text($.trim(newName));
		$("#hiddenTitle").val($.trim(newName));
	}

	if (newDescription == ""){
	$("#descriptionBox").text(defDescription);
	$("#hiddenDescription").val(defDescription);
	} else {
	$("#descriptionBox").text($.trim(newDescription));
	$("#hiddenDescription").val($.trim(newDescription));
	}
	
	$(".infoBox").prop('contenteditable','false');
	$(".infoBox").css({"backgroundColor":"#F5F5F5", "color":"inherit", "padding-right":"0px", "padding-left":"0px", "-webkit-border-radius":"8px","-moz-border-radius":"8px","border-radius":"8px"});
	});
});

});
    	