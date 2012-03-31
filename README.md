mindcollapse.com 
=============

##### Django code and static files for <http://www.mindcollapse.com/> and <http://www.mindcollapse.com/moho/>.

Requirements
------------

* Python > 2.3 (developed and tested on 2.7).
* Django 1.3.
* We use [Gunicorn WSGI Server](http://gunicorn.org/) and [Supervisord PCS](http://supervisord.org/).
* PostgreSQL or MySQL with version supported by Django.
* Nginx for serving static, you can find config example below.

Nginx config example
--------------------
	upstream prodbackend {
	        server unix:/home/mindcollapse/var/run/prod.socket;
	}
			
	server {
	        server_name www.mindcollapse.com;

	
	 		
	        location /media {
	                root /home/mindcollapse/www/;
	        }
	
	        location / {
	                root /home/mindcollapse/www/prod/static/;
	                try_files $uri @proxy_to_app;
	        }
	
	        location @proxy_to_app {
	            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	            proxy_set_header Host $http_host;
	            proxy_redirect off;
	            proxy_pass http://prodbackend;
	            proxy_intercept_errors on;
	        }
	
	        error_page 404 403 500 503 =404 /errors/gtfo.html;
	}
