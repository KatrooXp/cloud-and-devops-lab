## Docker task

Docker-compose.yml file is configured to do the next:

1. Starts php-ngnix web-server in "web" container on parameterized port (port is needed to be preset in .env file or environment variable) and mounts the project directory to /var/www/html
2. Starts mysql db in "db" container on parameterized port, takes db password from .env file, mounts database directory with script.sql to run the db and table creation, mounts external volume to store changes (to save changes if the containers are stopped or docker-compose stack is down)
3. Creates bridge network for these containers to work in it

* .env file contains port numbers and db password

![Alt text](<Screenshot from 2023-09-26 13-59-22.png>)

![Alt text](<Screenshot from 2023-09-26 13-58-58.png>)



