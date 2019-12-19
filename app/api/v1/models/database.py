import os

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    """Initialization."""

    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.conn = psycopg2.connect(database=self.db_name, host=self.db_host, user=self.db_user, password=self.db_password)
        self.curr = self.conn.cursor(cursor_factory=RealDictCursor)

    def create_table(self):
        """Create tables."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users(
                user_id serial PRIMARY KEY,
                firstname varchar NOT NULL,
                lastname varchar NOT NULL,
                surname varchar NOT NULL,
                admission_no varchar NOT NULL,
                email varchar NOT NULL,
                password varchar NOT NULL,
                form numeric NOT NULL,
                role varchar NOT NULL
            )""",
            """
            CREATE TABLE IF NOT EXISTS revoked_tokens(
                id serial PRIMARY KEY,
                jti varchar NOT NULL
            )""",
            """
            CREATE TABLE IF NOT EXISTS exams(
                exam_id serial PRIMARY KEY,
                admission_no varchar NOT NULL,
                term varchar NOT NULL,
                form numeric NOT NULL,
                type varchar NOT NULL,
                maths numeric NOT NULL,
                english numeric NOT NULL,
                kiswahili numeric NOT NULL,
                chemistry numeric NOT NULL,
                biology numeric NOT NULL,
                physics numeric NOT NULL,
                history numeric NOT NULL,
                geography numeric NOT NULL,
                cre numeric NOT NULL,
                agriculture numeric NOT NULL,
                business numeric NOT NULL,
                date TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS evaluation(
                comment_id serial PRIMARY KEY,
                name varchar NOT NULL,
                subject varchar NOT NULL,
                attendance varchar NOT NULL,
                homework varchar NOT NULL,
                rate varchar NOT NULL,
                comment varchar NOT NULL
            )""",
            """
            CREATE TABLE IF NOT EXISTS fees(
                fee_id serial PRIMARY KEY,
                admission_no varchar NOT NULL,
                transaction_type varchar NOT NULL,
                transaction_no varchar NOT NULL,
                description varchar NOT NULL,
                amount numeric NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS library(
                book_id serial PRIMARY KEY,
                admission_no varchar NOT NULL,
                book_no varchar NOT NULL,
                author varchar NOT NULL,
                title varchar NOT NULL,
                subject varchar NOT NULL
            )""",
            """
            CREATE TABLE IF NOT EXISTS studentId(
                student_id serial PRIMARY KEY,
                surname varchar NOT NULL,
                first_name varchar NOT NULL,
                last_name varchar NOT NULL,
                admission_no varchar NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS subjects(
                subject_id serial PRIMARY KEY,
                admission_no varchar NOT NULL,
                maths varchar NOT NULL,
                english varchar NOT NULL,
                kiswahili varchar NOT NULL,
                chemistry varchar NOT NULL,
                biology varchar NOT NULL,
                physics varchar NOT NULL,
                history varchar NOT NULL,
                geography varchar NOT NULL,
                cre varchar NOT NULL,
                agriculture varchar NOT NULL,
                business varchar NOT NULL
            )
            """
        ]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return e

    def create_admin(self):
        """Create a deafult admin user."""
        query = "INSERT INTO users(firstname,lastname,surname,admission_no,email, password,form,role)\
        VALUES('Harun','Gachanja','Gitundu','ADMF1001','harun@admin.com','pbkdf2:sha256:50000$aNlgJU9E$bf5d2dc9783e38f905618aacd50eb55b098f282dc6b03834aee7c4f80a9100e8','1','admin')"

        self.curr.execute(query)
        self.conn.commit()
        self.curr.close()

    def create_bursar(self):
        """Create a deafult admin user."""
        query = "INSERT INTO users(firstname,lastname,surname,admission_no,email, password,form,role)\
        VALUES('Samuel','Njoroge','Gitundu','ADMF2001','samuel@admin.com','pbkdf2:sha256:50000$MrtmQD9F$02db7419b111987ece6fae387f432bf875b4a34a4161c8e9ebf99f02c56258eb','2','admin')"

        self.curr.execute(query)
        self.conn.commit()
        self.curr.close()

    def destroy_table(self):
        """Destroy tables"""
        exams = "DROP TABLE IF EXISTS  exams CASCADE"
        users = "DROP TABLE IF EXISTS  users CASCADE"
        evaluation = "DROP TABLE IF EXISTS evaluation CASCADE"
        fees = "DROP TABLE IF EXISTS fees CASCADE"
        library = "DROP TABLE IF EXISTS library CASCADE"
        studentId = "DROP TABLE IF EXISTS studentId CASCADE"
        subjects = "DROP TABLE IF EXISTS subjects CASCADE"
        queries = [exams, users, evaluation, fees, library, studentId, subjects]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return e

if __name__ == '__main__':
    Database().destroy_table()
    Database().create_table()
    Database().create_admin()
    Database().create_bursar()

