#!/usr/bin/venv python
import os
from app import create_app, db
from app.models import User, Role, Interestedpeople, Permission, Product
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User,Permission=Permission, Role=Role, Interestedpeople=Interestedpeople, Product=Product)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User, Product, Interestedpeople

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()




if __name__ == '__main__':
    manager.run()
