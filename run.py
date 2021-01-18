import os

from app import exam_app


def app_context():
    if os.environ.get("FLASK_ENV") is None:
        application = exam_app('testing')
        return application
    application = exam_app(os.environ.get("FLASK_ENV"))
    return application


app = app_context()


if __name__ == '__main__':
    app.run()
