import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, DB
from user_model import *


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, DB)
manager = Manager(app)

manager.add_command('DB', MigrateCommand)


if __name__ == '__main__':
    manager.run()