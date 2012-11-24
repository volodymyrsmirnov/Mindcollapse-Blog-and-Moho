$(function(){

	$('h1,h2').click(function(){
	document.location.href = '/moho/'
	});

	$(window).scroll(function() {
		if ($(window).scrollTop() + 200 >= $(document).height() - $(window).height()) {
			if(scrollCount > 0 && disableAJAX == false) {
				$('#loading').show(); 
				disableAJAX = true;
				$.get('/moho/ajax/?type='+ajaxType+'&page='+scrollPage, function(data){

					if (history && history.pushState) {
						history.pushState(null, null, "/moho/page/"+ajaxType+"/"+scrollPage);
					}

					scrollCount -=7;
					$('#loading').hide();
					$('#reviews').append(data);
					scrollPage++;
					disableAJAX = false;
				});
			}
		}
	}); 

});