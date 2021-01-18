import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import exam_app, db
from app.api.v1.models.database import Database
from flask import redirect, make_response, jsonify


app = exam_app(os.environ.get('FLASK_ENV'))
app.app_context().push()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def destroy_tables_v1():
    """Drop tables if they exists."""
    Database().destroy_table()
    print("Version 1 existing tables destroyed...  OK")


@manager.command
def create_tables_v1():
    """Version 1: Create tables if they do not exists."""
    Database().create_table()
    print("Version 1 new tables created... OK")


@manager.command
def create_tables_v2():
    """Version 2 SQLAlchemy: Create tables if they do not exists."""
    db.create_all()
    print("Version 2 new tables created... OK")


@manager.command
def run():

    @app.route('/')
    def index():
        return make_response(jsonify({
            "message": "Welcome to ATC. Best Tech Best Future.",
            "status": "OK"
        }), 200)

    @app.route('/docs')
    def docs():
        return redirect('https://portal56.docs.apiary.io/', code=302)

    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()