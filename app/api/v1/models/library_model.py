import json
import psycopg2

from app.api.v1.models.database import Database

from datetime import datetime


class LibraryModel(Database):
    """Initiallization."""

    def __init__(
            self,
            admission_no=None,
            title=None,
            author=None,
            book_no=None,
            created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.title = title
        self.author = author
        self.book_no = book_no
        self.created_on = datetime.now()

    def save(self):
        """Add a new book."""
        try:
            self.curr.execute(
                ''' INSERT INTO library(student, title, author, book_no, created_on)
                VALUES('{}','{}','{}','{}','{}')
                RETURNING student, title, author, book_no, created_on'''
                .format(self.admission_no, self.title, self.author, self.book_no, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_all_books(self):
        """Fetch all books."""
        query = "SELECT u.admission_no, u.firstname, u.lastname, u.surname,\
                          l.title, l.author, l.book_no FROM library AS l\
                          INNER JOIN users AS u ON l.student = u.admission_no"
        response = Database().fetch(query)
        return response

    def get_books_by_user_admission(self, admission_no):
        """Get a book with specific user admission."""
        self.curr.execute(""" SELECT u.admission_no, u.firstname, u.lastname, u.surname,
                          l.title, l.author, l.book_no FROM library AS l
                          INNER JOIN users AS u ON l.student = u.admission_no
                          WHERE admission_no=%s""", (admission_no,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def edit_books(self, book_id, title, author, book_no):
        """Edit books."""
        self.curr.execute("""UPDATE library
			SET title='{}', author='{}', book_no='{}'
			WHERE book_id={} RETURNING title, author, book_no"""
                          .format(book_id, title, author, book_no))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
