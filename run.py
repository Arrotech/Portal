import os

from app import exam_app
from app.api.v1.models.database import Database
from utils.serializer import Serializer

app = exam_app('testing')


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

# @app.cli.command()
# def create_registrar():
#     """Create tables if they do not exists."""
#     Database().create_registrar()


if __name__ == '__main__':
    app.run()