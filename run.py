import os
from flask import make_response, jsonify, redirect
from app import exam_app

app = exam_app(os.environ.get("FLASK_ENV", 'production'))


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
