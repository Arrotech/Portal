import os

from app import exam_app
from flask_jwt_extended import JWTManager
from app.api.v1.models.database import Database

config_name = os.getenv('APP_SETTINGS')
app = exam_app(config_name)


if __name__ == '__main__':
    app.run(debug=True)
