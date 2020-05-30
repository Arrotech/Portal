import json

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.api.v1.models.library_model import LibraryModel
from app.api.v1.models.users_model import UsersModel
from utils.authorization import admin_required
from utils.utils import check_library_keys, raise_error, check_edit_library_keys
from utils.serializer import Serializer
from app.api.v1 import books_v1


@books_v1.route('/books', methods=['POST'])
@jwt_required
@admin_required
def add_book():
    """Add a new book."""
    errors = check_library_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    title = details['title']
    author = details['author']
    book_no = details['book_no']
    if UsersModel().get_user_by_admission(admission_no):
        response = LibraryModel(admission_no,
                                title,
                                author,
                                book_no).save()
        if "error" in response:
            return raise_error(404, "Student not found")
        return Serializer.serialize(response, 201, "Book added successfully")


@books_v1.route('/books', methods=['GET'])
@jwt_required
@admin_required
def get_books():
    """Fetch all books."""
    response = LibraryModel().get_all_books()
    return Serializer.serialize(response, 200, "Books retrieved successfully")


@books_v1.route('/books/<string:admission_no>', methods=['GET'])
@jwt_required
def get_books_for_one_student_by_admission(admission_no):
    """Fetch books for a single student by admission."""
    response = LibraryModel().get_books_by_user_admission(admission_no)
    if response:
        return Serializer.serialize(response, 200, "Books retrieved successfully")
    return raise_error(404, "Student not found")


@books_v1.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required
@admin_required
def put(book_id):
    """Edit books."""
    errors = check_edit_library_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    title = details['title']
    author = details['author']
    book_no = details['book_no']
    response = LibraryModel().edit_books(title, author, book_no, book_id)
    if response:
        return Serializer.serialize(response, 200, "Book updated successfully")
    return raise_error(404, "Book not found")
