### Dockerized Hello World API Server using Nginx, Redis, Django


The components of the directory are 
- /Helloworld, the root of the django project 
- /nginx,
	- Dockerfile, contains the image creation commands for nginx 
	- nginx.conf,  nginx server configuration file
- docker-compose.yml, describes the services that need to be launched 
- Dockerfile, the docker image creation file for django web server


The Nginx webserver redirects the requests to the WSGI Server of django, in which the / points to the webpage that displays the visual logs and the per minute api requests from each Ip address

Used Django for creating the web service.

Redis stores the logs for each interaction with the API, and is used to display the details for the internal users of the system


###### Nice to have Improvements

- OAUTH2 based access
- Sigin in the webpage
- Optimize per minute statistics display 

