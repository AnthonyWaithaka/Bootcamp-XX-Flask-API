# manage.py

import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.app import db, create_app
from app import models

app = create_app(config_name=os.getenv('APP_SETTINGS','development'))
migrate = Migrate(app, db)
manager = Manager(app)

#migration command will always be preceded by the word "db"
#Usage: python manage.py db init*
#Usage: replace init with migrate or upgrade
manager.add_command('db', MigrateCommand)

#command for testing
#Usage: python manage.py test
@manager.command
def test():
    """Run unit tests without test coverage
    """
    tests = unittest.TestLoader().discover('./test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
