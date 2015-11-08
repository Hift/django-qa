		jQuery(document).ready(function(){
		jQuery(".login-url").click(function(){
			jQuery("#login_register").load("http://127.0.0.1:8000/login/login.html");
		})
	})