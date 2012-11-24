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



					scrollCount -=7;
					$('#loading').hide();
					$('#reviews').append(data);
					scrollPage++;
					disableAJAX = false;
				});


				if (history && history.replaceState) {
					history.replaceState(null, null, "/moho/page/?type="+ajaxType+'&page='+scrollPage);
				}

			}
		}
	}); 

});