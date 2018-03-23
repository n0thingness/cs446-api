import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import APP, DB
from user_db import *
from location_db import *


APP.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(APP, DB)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()