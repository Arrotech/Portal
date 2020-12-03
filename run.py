import os

from app import exam_app
from app.api.v1.models.database import Database
from utils.serializer import Serializer

app = exam_app('testing')


@app.cli.command()
def destroy():
    """Delete tables on the terminal."""
    Database().destroy_table()


if __name__ == '__main__':
    app.run()