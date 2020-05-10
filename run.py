import os

from app import exam_app
from app.api.v1.models.database import Database
from utils.serializer import Serializer

config_name = os.getenv('APP_SETTINGS')
app = exam_app(config_name)


@app.cli.command()
def create():
    Database().create_table()


@app.cli.command()
def destroy():
    Database().destroy_table()


if __name__ == '__main__':
    app.run()
