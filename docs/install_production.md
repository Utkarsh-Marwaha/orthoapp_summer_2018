# Installing Django on techbroker.cecs.anu.edu.au

These instructions acn be used tio install the TechBroker system on the techbroker.cecs.anu.edu.au server

## Development environment

Install the development environment as detailed in [install_development.md](https://gitlab.anu.edu.au/u4022606/techbroker-django/blob/master/doc/install_development.md).
	
	
## Production Deployment

### Install and test gunicorn

Install

	sudo pip install gunicorn
	
Edit settings.py - add host to ALLOWED_HOSTS

	ALLOWED_HOSTS = ['techbroker.cecs.anu.edu.au']

Test it via a browser. Note that static files aren't available, so there is no CSS etc.

	http://techbroker.cecs.anu.edu.au

### Install and test nginx

The world will talk to nginx which will talk to gunicorn. It will also serve static files.

Install

	sudo apt-get install nginx
	
Link the config file

	cd /etc/nginx/sites-enabled
	sudo ln -s $TECHBROKER_HOME/conf/nginx.conf orthoapp

Start nginx

	sudo systemctl restart nginx

Test it via a browser. You will see the *Welcome to nginx!* page.

	http://techbroker.cecs.anu.edu.au
	
### Start the production server

	./start_prod_server.sh
	
This script will restart nginx and then runs gunicorn.

Test it via a browser. You will see the TechBroker app.

	http://techbroker.cecs.anu.edu.au


