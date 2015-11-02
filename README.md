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

### Api

This api was created specifically to feed the [Markets](http://codeforamerica.github.io/westsac-farmers-and-markets/#/home) App. Although is open for other developers to explore and try new ideas with this data.

> Note: this data is not updated

#### get all users

```
http://westsacramentourbanfarm.com/api/users/
```
result: 

```javascript
{
    "ajgomez@mail.ru": {
        "about_me": null, 
        "email": "ajgomez@mail.ru", 
        "farm_name": null, 
        "id": 17, 
        "last_seen": "2015-07-29T22:50:09.099814+00:00", 
        "location": null, 
        "member_since": "2015-07-29T22:50:09.099814+00:00", 
        "name": "AJ Gomez", 
        "phone": null, 
        "products": [], 
        "url": null
      }, 
      "fredricblum@gmail.com": {
        "about_me": null, 
        "email": "fredricblum@gmail.com", 
        "farm_name": null, 
        "id": 11, 
        "last_seen": "2015-07-29T22:45:58.786206+00:00", 
        "location": null, 
        "member_since": "2015-07-29T22:45:58.786206+00:00", 
        "name": "Fred Blum", 
        "phone": null, 
        "products": [], 
        "url": null
      },
      ...
}

```

#### get a single user
```
http://westsacramentourbanfarm.com/api/users/3
```

result: 

```javascript
{
  "about_me": null, 
  "email": "ajgomez@mail.ru", 
  "farm_name": null, 
  "id": 17, 
  "last_seen": "2015-07-29T22:50:09.099814+00:00", 
  "location": null, 
  "member_since": "2015-07-29T22:50:09.099814+00:00", 
  "name": "AJ Gomez", 
  "phone": null, 
  "products": [], 
  "url": null
}

```

How to use it?
--------------

### About

In the city of West Sacramento the City Government as well as the Center for Land Base Learning are promoting initiatives related to urban farming. As part of the Code for America Fellowship 2015, Team West Sacramento, we created [Acres](http://acres.online/) which help aspiring new farmers to find the land they need.
Farm Stand was design to help urban farmers to create a awareness in their community about the produce they are growing and the times for people to buy those.

### Resgistration

Any farmer can register going to the bottom left corner and click on login.

1. At the end of the form there is a link that says *Sing Up* click on it and with just the email, you will be able to sign up.
2. Once the user registers, they will receive an email with a link to confirm the ownership of that email. The user should click the link and login in the app.



### Edit Profile
If the user is not in the Crop List page already:

1. Go to the bottom left corner of the front page and click on the link named *Crop List*. 
2. In the menu bar you will find a link to your Profile, click there.
3. You just click where it says *Edit Profile* and this will take the user to a form where will be able to their farm name and their website.
4. Click *Save* and your profile will be complete.


### Adding a Produce 
Adddinga a produce is very easy.

1. On the menu bar, the user should navegate to the Crop List page through the clicking of the *Crop List* link.
2. Click in the plus icon ubicated in the right top corner or the list.
3. The user should fill all the fields on the form and click Submit. This will take the user to the Crop List again where will be able to verify the produce that has been just submited. 

note: to edit the information of the produce, the user just have to click on the pencil icon floating right of the name of the produce and this will take them to the same form that we just describe for adding produce.









