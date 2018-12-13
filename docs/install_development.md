# Installing the development environment

These instructions can be used to install the software required to develop the TechBroker system.

These instructions cover Debian based Linux distribution (eg. Ubuntu, Mint etc.) and Apple OSX. 

No attempt has been made to setup a Windows system - Windows is a mystery to me !

## Foundations

### Assumptions

* You are running a debian-based Linux distribution or OSX (tested on Mojave)
* You have access to the **techbroker-django** repo on gitlab.anu.edu.au

### Install Python3

Python 2 is probably the default. We want to use Python 3. So:

	Linux
		$ sudo update-alternatives --remove python /usr/bin/python2
		$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1

	OSX
		Download and run the latest Python3 installer from 
		https://www.python.org/downloads/mac-osx/
		

	
Check that python3 is OK

	$ python3
	Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28)
	[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>>

Install pip3

	Linux
		$ sudo apt-get install python3-pip
		$ sudo ln -s /usr/bin/pip3 /usr/bin/pip

	OSX
		Should already be installed
		
Check that pip3 is OK

	$ pip3 -V
	pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.5)
	$
	
## Install less

We use [Less.js](http://lesscss.org/) to manage our CSS files. Install using:

	Linux
		$ sudo apt-get install npm
		$ sudo npm install -g less
	
	OSX
		Should already be installed
		
Test

	$ lessc -v
	
If this fails on Linux by not finding 'node', then you may need to:

	$ sudo ln -s /usr/bin/nodejs /usr/bin/node
	
### Install Django

Install django

	$ sudo pip3 install django

Check that django is OK

	$ python3
	Python 3.5.3 (default, Jan 19 2017, 14:11:04)
	[GCC 6.3.0 20170118] on linux
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import django
	>>> print(django.get_version())
	2.0.4
	>>>
	
Install the [postgreSQL wrapper stuff](http://initd.org/psycopg/docs/install.html)

	$ pip3 install psycopg2-binary
	
Install [pillow](https://pypi.org/project/Pillow/) - image processing stuff 

	$ pip3 install pillow

Install [django_extensions](https://github.com/django-extensions/django-extensions)

	$ pip3 install django-extensions
	
Install [markdown2](https://github.com/svetlyak40wt/django-markdown2)

	$ pip3 install markdown2
	$ pip3 install django-markdown2
	
Install [django-model-utils](https://github.com/jazzband/django-model-utils)
	
	$ pip3 install django-model-utils
	
(optional) Install [graphviz](http://www.graphviz.org) - required to use the *graph_database.sh* script

Note that, if you are using OSX, you will need to install [homebrew](https://brew.sh).

	Linux
		$ sudo apt-get install graphviz libgraphviz-dev
	
	OSX
		$ brew install graphviz
		
	$ pip3 install pygraphviz
	$ pip3 install pydotplus
	

### Install postgreSQL

Install postgreSQL

	Linux
		$ sudo apt-get install postgresql

	OSX
		Install Postgres.app as per documentation at https://postgresapp.com
		
Setup the techbroker database

	$ sudo su - postgres
	postgres@techbroker:~$ psql
	psql (9.6.7)
	Type "help" for help.

	postgres=# CREATE DATABASE techbroker;
	CREATE DATABASE
	postgres=# CREATE USER techbroker WITH PASSWORD 'your_password';
	CREATE ROLE
	postgres=# ALTER ROLE techbroker SET client_encoding TO 'utf8';
	ALTER ROLE
	postgres=# ALTER ROLE techbroker SET default_transaction_isolation TO 'read committed';
	ALTER ROLE
	postgres=# ALTER ROLE techbroker SET timezone TO 'UTC';
	ALTER ROLE
	postgres=# GRANT ALL PRIVILEGES ON DATABASE techbroker TO techbroker;
	GRANT
	postgres=# \q
	postgres@techbroker:~$ exit
	logout	

	
	
### Install git

Git may not be installed on Linux, so:

	Linux
		$ sudo apt-get install git
	
### Clone techbroker-django repo

Make sure you have your ssh keys setup, and then clone the repo:

	$ git clone git@gitlab.anu.edu.au:TechBroker/techbroker-django.git

### 	Setup the techbroker database

Go to where the techbroker django system is:

	$ cd <TechBroker path>/techbroker-django/techbroker/
	
Create the database

	$ python3 manage.py migrate
	
## Running the development server

Note that this should only be used for development. See [install_production.md](https://gitlab.anu.edu.au/u4022606/techbroker-django/blob/master/doc/install_production.md) for production instructions.

Go to where the techbroker scripts are:

	$ cd <TechBroker path>/techbroker-django/techbroker/scripts
	
Create and run a script to setup development environment

	$ cp production_template.sh production.sh
	
	edit production.sh to set the TECHBROKER_HOME variable to
	<TechBroker path>/techbroker-django/techbroker
	
	$ source ./development.sh
	
Generate a secret key

	$ ./genSecretKey.sh
	
	edit production.sh and replace the existing SECRET_KEY with the new key
	
	$ source ./development.sh
	$ ./start_dev_server.sh
	

