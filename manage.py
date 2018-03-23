import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import APP, DB
from user_model import *


APP.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(APP, DB)
manager = Manager(app)

manager.add_command('DB', MigrateCommand)


if __name__ == '__main__':
    manager.run()