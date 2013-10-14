$(function(){
	Hyphenator.run({
		remoteloading: false,
		useCSS3hyphenation: true,
	});

	$(".content img").addClass("img-responsive");

	$(".social a").click(function(e){
		e.preventDefault();
		window.open ($(this).attr("href"), $(this).attr("title"), "location=0,status=0,scrollbars=0,width=640,height=480");
	})
});