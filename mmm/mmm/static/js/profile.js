$(document).ready(function(){
$("#editButton").click(function(){
	$(".profPic").click(function(){
	$(".picChange").trigger("click");
	});
	$(".profPic").css({"border":"gray dotted"});
	var aboutText = $("#aboutBox").text();
	var nameText = $(".name").text();
	var majorText = $(".major").text();
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
	$("#cancelButton").click(function(){
		$(".profPic").unbind();
					$(".profPic").css({"border":"none"});


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
		$(".profPic").unbind();
			$(".profPic").css({"border":"none"});


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
		$("#hiddenName").val($.trim(newName));
	} else {
		$(".name").text($.trim(newName));
		$("#hiddenName").val($.trim(newName));
	}
	if (newMajor == ""){
		$(".major").text(defMajor);
		$("#hiddenMajor").val(defMajor);
	} else {
		$(".major").text($.trim(newMajor));
		$("#hiddenMajor").val($.trim(newMajor));
	}
	if (newAbout == ""){
		$("#aboutBox").text(defAbout);
		$("#hiddenAbout").val(defAbout);
		} else {
		$("#aboutBox").text($.trim(newAbout));
		$("#hiddenAbout").val($.trim(newAbout));
	}

	$('form#profileEditForm').submit();
	
	$(".infoBox").prop('contenteditable','false');
	$(".infoBox").css({"backgroundColor":"#F5F5F5", "color":"inherit", "padding-right":"0px", "padding-left":"0px", "-webkit-border-radius":"8px","-moz-border-radius":"8px","border-radius":"8px"});
	});
});

});