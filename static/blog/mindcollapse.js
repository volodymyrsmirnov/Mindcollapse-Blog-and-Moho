$(function(){
	Hyphenator.config({
		remoteloading: false,
		useCSS3hyphenation: true,
	});

	Hyphenator.run();

	$(".content img").addClass("img-responsive");

	$(".social a").click(function(e){
		e.preventDefault();
		window.open ($(this).attr("href"), $(this).attr("title"), "location=0,status=0,scrollbars=0,width=640,height=480");
	})
});