import json
import psycopg2

from app.api.v1.models.database import Database

from datetime import datetime


class LibraryModel(Database):
    """Initiallization."""

    def __init__(
            self,
            user_id=None,
            title=None,
            author=None,
            book_no=None,
            date=None):
        super().__init__()
        self.user_id = user_id
        self.title = title
        self.author = author
        self.book_no = book_no
        self.date = datetime.now()

    def save(self):
        """Add a new book."""
        try:
            self.curr.execute(
                ''' INSERT INTO library(student, title, author, book_no, date)
                VALUES('{}','{}','{}','{}','{}')
                RETURNING student, title, author, book_no, date'''
                .format(self.user_id, self.title, self.author, self.book_no, self.date))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_all_books(self):
        """Fetch all books."""
        self.curr.execute(''' 
                          SELECT users.admission_no, title, author, book_no FROM library
                          INNER JOIN users ON library.student = users.user_id
                          ''')
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_books_by_user_id(self, user_id):
        """Get a book with specific user id."""
        self.curr.execute(""" 
                          SELECT users.admission_no FROM library
                          INNER JOIN users ON library.student = users.user_id 
                          WHERE user_id={}""".format(user_id))
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
