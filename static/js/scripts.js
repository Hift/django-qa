jQuery(document).ready(function(jQuery) {

	if( jQuery("#answers_filter").length > 0 ){
		jQuery('#answers_filter').waypoint('sticky', {
			stuckClass: 'stuck-sticky',
			wrapper: '<div class="sticky-wrapper" />'
		});
	}

	if( jQuery("#question_filter").length > 0 ){
		jQuery('#question_filter').waypoint(function(direction) {
			//console.log('aaa');
			if(direction == "down"){
				jQuery('#p_change').appendTo('#to_add1');
				jQuery('#q_filter_waypoints').fadeIn();
			}
			else{
				jQuery('#p_change').appendTo('#to_add2');
				jQuery('#q_filter_waypoints').fadeOut('fast');
			}	
		}, { offset: 0 });
	}
});