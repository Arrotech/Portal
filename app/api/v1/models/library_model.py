import json

from app.api.v1.models.database import Database

from datetime import datetime

Database().create_table()


class LibraryModel(Database):
    """Initiallization."""

    def __init__(
            self,
            admission_no=None,
            book_no=None,
            author=None,
            title=None,
            subject=None,
            form=None,
            stream=None,
            date=None):
        super().__init__()
        self.admission_no = admission_no
        self.book_no = book_no
        self.author = author
        self.title = title
        self.subject = subject
        self.form = form
        self.stream =stream
        self.date = datetime.now()

    def save(self):
        """Add a new book."""

        self.curr.execute(
            ''' INSERT INTO library(admission_no, book_no, author, title, subject, form, stream, date)\
            VALUES('{}','{}','{}','{}','{}','{}','{}','{}')\
             RETURNING admission_no, book_no, author, title, subject, form, stream, date''' \
                .format(self.admission_no, self.book_no, self.author, self.title, self.subject, self.form, self.stream, self.date))
        book = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(book, default=str)

    def get_all_books(self):
        """Fetch all books."""

        self.curr.execute(''' SELECT * FROM library''')
        books = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(books, default=str)

    def get_books_by_admission_no(self, admission_no):
        """Get an exam with specific admission no."""
        self.curr.execute(""" SELECT * FROM library WHERE admission_no=%s""", (admission_no,))
        book = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(book, default=str)

    def edit_books(self, book_id, admission_no, book_no, author, title, subject, form, stream):
        """Edit books."""

        self.curr.execute("""UPDATE library\
			SET admission_no='{}', book_no='{}', author='{}', title='{}', subject='{}', form='{}', stream='{}'\
			WHERE book_id={} RETURNING admission_no, book_no, author, title, subject, form, stream"""
            .format(book_id, admission_no, book_no, author, title, subject, form, stream))
        book = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(book, default=str)
