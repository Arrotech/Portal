import os
from flask import make_response, jsonify, redirect
from app import exam_app


def app_context():
    if os.environ.get("FLASK_ENV") is None:
        application = exam_app('testing')
        return application
    application = exam_app(os.environ.get("FLASK_ENV"))
    return application


app = app_context()


@app.route('/')
def index():
    return make_response(jsonify({
        "message": "Welcome to ATC. Best Tech Best Future.",
        "status": "OK"
    }), 200)


@app.route('/docs')
def docs():
    return redirect('https://portal56.docs.apiary.io/', code=302)


if __name__ == '__main__':
    app.run()
