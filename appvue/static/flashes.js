$(document).ready(function(){
	$('div.alert button').on('click', function(){
		$(this).parent().slideUp(500, function(){
			$(this).remove()
		})
	})
})