var ismobile = false;

if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
	ismobile = true;
}

document.onkeydown = LeftRightNavigate;

function LeftRightNavigate(event) {

	if (window.event) event = window.event;

	if (event.ctrlKey) {
	
		var link = null;
		
		switch (event.keyCode ? event.keyCode : event.which ? event.which : null){
		
			case 0x25:
				link = document.getElementById ('prevlink');
				break;
			case 0x27:
				link = document.getElementById ('nextlink');
				break;
				
		}

		if (link && link.href) document.location = link.href;
	}			
}

$(function(){

	// Social share buttons
	$(".social a").click(function(e){
		e.preventDefault();
		window.open ($(this).attr('href'), $(this).attr('title'),"location=0,status=0,scrollbars=0,width=640,height=480");
	})


	if (!ismobile) {

		// Hide paginations links if display resolution width is less then 1050
		$(window).resize(function() {
			if ($(window).width() < 1050)
				$('.pagination_link').hide();
			else
				$('.pagination_link').show();
		});

		$(window).trigger('resize');

		// Sliding post headers
		$(document).scroll(function(e){
			var scroll_top = $(document).scrollTop();

			$('.article').each(function(id, article){

				var article = $(article);

				article.find('.header').css('z-index', id);

				var scroll_zone = {
					'top':article.position().top + 23,
					'bottom': article.position().top + article.height() + 100
				}

				if (scroll_top > scroll_zone.top && scroll_top < scroll_zone.bottom) {
					article.find('.header').css('position', 'fixed').css('top', 0);
					article.find('.description').css('padding-top', '55px');
				} else {
					article.find(".header").css('position', 'relative');
					article.find(".description").css('padding-top', '8px');
				}

			})
		});
	} 
	else {

		$('.pagination_link').hide();
	}
})
