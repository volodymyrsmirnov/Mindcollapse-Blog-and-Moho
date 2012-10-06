$(function(){
	// OLD CLEDITOR 
	//$('.mohos-moho.change-form #id_text').cleditor({width:'800', height:'300'});	
	//$('.blogs-post.change-form #id_text').cleditor({width:'900', height:'700'});
	$('.blogs-post.change-form #id_text').redactor({ 
		minHeight: 700,
		wym: true,
		fixedBox: true,
		fixed: true
	}); 

});
