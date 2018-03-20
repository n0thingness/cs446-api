# cs446-api

Remember to install autoenv outside of your virtual env

Create a .env file in root directory

Add following info:

```
source env/Scripts/activate
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://postgres:DB_PASSWORD@localhost/DB_NAME"
```

Be sure to modify the first line to suit your system appropriately, currently it is for the Windows implementation of virtual env

Code for migrating database:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

First line is for initializing migrations folder (run once)

Second line is for creating a new migration to update the db model (run when model is changed)

Third line is for upgrading the db to the latest migration
