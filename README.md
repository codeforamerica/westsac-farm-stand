===============================
West Sacramento Farm Stand
===============================

Getting Started
----------------

You will need to have Postgres SQL Installed on your machine ([You can get it here](http://www.postgresql.org/download)) and you will need to have it started and create a admin user with priviledges:

```
    $ psql 
```

```
    # CREATE USER admin;
    # CREATE DATABASE farm_stand;
    # ALTER DATABASE farm_stand OWNER TO admin;
    # \q
```

Then run the following commands to bootstrap your environment:


```
    $ git clone https://github.com/codeforamerica/westsac-farm-stand.git
    $ cd westsac-farm-stand/
```

Now, you'll need to install the virtualenv [see instructions](https://virtualenv.readthedocs.org/en/latest/installation.html) tool and then setup the environment:


```
    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt
```

Finally, you'll want to initialize the database and start the server:

```
    (venv)$ python manage.py db init
    (venv)$ python manage.py db migrate
    (venv)$ python manage.py db upgrade 
    (venv)$ python manage.py server
```

*(venv) means that the virtualenv is activated*

You should then be able to view the app at localhost:5000 in your local web browser.


Shell
-----

To open the interactive shell, run 
```
    (venv)$ python manage.py shell
```


Migrations
----------

Whenever a database migration needs to be made. Run the following commmands:
```
    (venv)$ python manage.py db migrate
```

This will generate a new migration script. Then run:
```
    (venv)$ python manage.py db upgrade
```

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
