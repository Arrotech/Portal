import os

from flask import redirect, make_response, jsonify
from app import exam_app
from app.api.v1.models.database import Database
from utils.serializer import Serializer

app = exam_app('testing')


# Create app instance with env
def app_context():
    if os.getenv("FLASK_ENV") is None:
        application = exam_app('testing')
        return application
    application = exam_app(os.getenv("FLASK_ENV"))
    return application


app = app_context()


@app.cli.command()
def destroy_tables():
    """Create tables if they do not exists."""
    Database().destroy_table()
    print("Existing tables destroyed...")


@app.cli.command()
def create_tables():
    """Create tables if they do not exists."""
    Database().destroy_table()
    print("Existing tables destroyed...")
    Database().create_table()
    print("New tables created...")

@app.route('/docs')
def home():
    return redirect('https://portal56.docs.apiary.io/#', 302,
                    make_response(jsonify({"message": "redirecting to documentation"})))



if __name__ == '__main__':
    app.run()