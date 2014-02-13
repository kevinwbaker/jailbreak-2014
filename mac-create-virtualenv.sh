#!/bin/bash

new_install=false

if [ ! -d "env" ]; then

	#
	# Check if Homebrew is installed
	#
	which -s brew
	if [[ $? != 0 ]] ; then
		# Install Homebrew
		# https://github.com/mxcl/homebrew/wiki/installation
		/usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
	else
		brew update
	fi

	which -s mysql || brew install mysql
	which -s python || brew install python --with-brewed-openssl
	which -s virtualenv || pip install virtualenv

	#Setting up virtualenv

    if [ ! -d "env" ]; then
        mkdir "env"
    fi
	
    virtualenv --no-site-packages "env"

	source "env/bin/activate"

	#
	# Install application requirements
	#
	pip install -r requirements.txt || { echo ' === localrun failed. pip could not installed the required files. === ' ; exit 1; }
else
	source "env/bin/activate"
fi


if [ ! -f "project/database.sqlite3" ]; then
	new_install=true
fi
( cd project ; python manage.py syncdb --noinput);
( cd project ; python manage.py migrate);

if $new_install ; then
	echo ' ==== First Time Setup - Create an Administration Account ==== '; 
	( cd project ; python manage.py createsuperuser );
fi
( cd project ; python manage.py runserver );