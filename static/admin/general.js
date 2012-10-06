$(function(){
	$('.blogs-post.change-form #id_text').redactor({ 
		minHeight: 700,
		wym: true,
		fixedBox: true,
		fixed: true,
		imageUpload: '/godmode/blog_upload_file',
		fileUpload: '/godmode/blog_upload_file',
		callback: function(){$('.redactor_box').css('width','900px')},
		autosave: '/godmode/blog_autosave_post', 
        interval: 60,
        autosaveCallback: function(data) {console.log("Post autosaved with data", data)}

	}); 

	/* dont need any WYSIWYG in MOHO, disable it 
	$('.mohos-moho.change-form #id_text').redactor({ 
		minHeight: 300,
		wym: true,
		fixedBox: true,
		fixed: true
	}); 

	*/

	

});
