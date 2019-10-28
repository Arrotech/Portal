import json

from app.api.v1.models.database import Database

Database().create_table()


class LibraryModel(Database):
    """Initiallization."""

    def __init__(
            self,
            admission_no=None,
            book_no=None,
            author=None,
            title=None,
            subject=None):
        super().__init__()
        self.admission_no = admission_no
        self.book_no = book_no
        self.author = author
        self.title = title
        self.subject = subject

    def save(self):
        """Add a new book."""

        self.curr.execute(
            ''' INSERT INTO library(admission_no, book_no, author, title, subject)\
            VALUES('{}','{}','{}','{}','{}')\
             RETURNING admission_no, book_no, author, title, subject''' \
                .format(self.admission_no, self.book_no, self.author, self.title, self.subject))
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
