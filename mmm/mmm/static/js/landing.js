$(document).ready(function(){

  		$('.blur').bind("cut copy paste",function(e) {
    	  e.preventDefault();
  		});
  	
  		$('.feedItem').mouseover(function(){
  		$(this).children('.prompt').show();
  		$(this).children('.blur').css("z-index", "1");

  		//$(this).children('.blur').hide();
  		
  		});
  		$('.feedItem').mouseout(function(){
  		$(this).children('.prompt').hide();
  		$(this).children('.blur').css("z-index","3");
  		});
  		$(".goToLogin").click(function(){
    		window.location.href = "login.html";
    		//alert("why does this only work with an alert?");
    		});
    		
    		$('.blur').each(function(){
    		var count = 0;
    		var html=$(this).html();
    		var newHtml='';
    		for (var i=0;i<html.length;i++) {
        		newHtml=newHtml+html[i];
        		if ((i+1)%73==0) {
        		count = count+1;
        		if (count == 4){
        		var lastIndex = newHtml.lastIndexOf(" ")

			newHtml = newHtml.substring(0, lastIndex);
        		newHtml = newHtml + "xx-xx"+'<br/>';
        		}else{
        		//newHtml=newHtml+'<br/>';
        		 }
        		 }
    		if (count == 4) {
    		newHtml = newHtml.substring(0, newHtml.indexOf("xx-xx"));
    			newHtml = newHtml + "...";
			$(this).html(newHtml);
			break;
    		}
    		$(this).html(newHtml);
    		$(this).parent().parent().height($(this).parent().height() + 50);
		};
		});
		
  		
  	
	});
	