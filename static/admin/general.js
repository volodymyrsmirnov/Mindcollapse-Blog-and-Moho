$(function(){

	post_id = document.location.pathname.match(/\/godmode\/blogs\/post\/(.*)\//);
	if (post_id != null) post_id = post_id[1];
	else post_id = "new";

	$('.blogs-post.change-form #id_text').redactor({ 
		minHeight: 500,
		wym: true,
		fixedBox: true,
		fixed: true,
		imageUpload: '/godmode/blog_upload_file',
		fileUpload: '/godmode/blog_upload_file',
		callback: function(){$('.redactor_box').css('width','900px')},
		autosave: '/godmode/blog_autosave_post?post_id=' + post_id, 
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
