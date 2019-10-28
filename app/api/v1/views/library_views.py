import json

from flask import request, jsonify, make_response, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.api.v1.models.library_model import LibraryModel
from utils.authorization import admin_required

books_v1 = Blueprint('books_v1', __name__)


@books_v1.route('/books', methods=['POST'])
@jwt_required
@admin_required
def add_book():
    """Add a new book."""
    details = request.get_json()
    admission_no = details['admission_no']
    book_no = details['book_no']
    author = details['author']
    title = details['title']
    subject = details['subject']
    book = LibraryModel(admission_no,
                        book_no,
                        author,
                        title,
                        subject).save()
    book = json.loads(book)
    return make_response(jsonify({
        "status": "201",
        "message": "Book awarded successfully",
        "book": book
    }), 201)

@books_v1.route('/books', methods=['GET'])
@jwt_required
def get_books():
    """Fetch all books."""
    return make_response(jsonify({
        "status": "200",
        "message": "Retrieved successfully",
        "books": json.loads(LibraryModel().get_all_books())
    }), 200)

@books_v1.route('/books/<string:admission_no>', methods=['GET'])
@jwt_required
def get_book(admission_no):
    """Fetch a book."""
    book = LibraryModel().get_books_by_admission_no(admission_no)
    book = json.loads(book)
    if book:
        return make_response(jsonify({
            "status": "200",
            "message": "Retrieved successfully",
            "Book": book
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "Book Not Found"
    }), 404)
