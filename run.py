import os

from flask import redirect, make_response, jsonify
from app import exam_app
from app.api.v1.models.database import Database


def app_context():
    if os.getenv("FLASK_ENV") is None:
        application = exam_app('testing')
        return application
    application = exam_app(os.environ.get("FLASK_ENV"))
    return application


app = app_context()


@app.cli.command()
def destroy_tables():
    """Create tables if they do not exists."""
    Database().destroy_table()
    print("Existing tables destroyed...  OK")


@app.cli.command()
def create_tables():
    """Create tables if they do not exists."""
    Database().destroy_table()
    print("Existing tables destroyed... OK")
    Database().create_table()
    print("New tables created... OK")
    Database().create_registrar()
    print("Registrar account created successfully... OK")


@app.route('/')
def index():
    return make_response(jsonify({
        "message": "Welcome to your institution portal",
        "status": "200"
    }), 200)


@app.route('/docs')
def docs():
    return redirect('https://portal56.docs.apiary.io/', code=302)


if __name__ == '__main__':
    app.run()
