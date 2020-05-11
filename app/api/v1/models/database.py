import os
import json

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    """Initialization."""

    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.conn = psycopg2.connect(
            database=self.db_name, host=self.db_host, user=self.db_user, password=self.db_password)
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
                stream varchar NOT NULL,
                role varchar NOT NULL,
                date TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS staff(
                staff_id serial PRIMARY KEY,
                firstname varchar NOT NULL,
                lastname varchar NOT NULL,
                form varchar NOT NULL,
                stream varchar NOT NULL,
                username varchar NOT NULL,
                email varchar NOT NULL,
                password varchar NOT NULL,
                role varchar NOT NULL,
                date TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS accountants(
                accountant_id serial PRIMARY KEY,
                firstname varchar NOT NULL,
                lastname varchar NOT NULL,
                username varchar NOT NULL,
                email varchar NOT NULL,
                password varchar NOT NULL,
                role varchar NOT NULL,
                date TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS units(
                unit_id serial PRIMARY KEY,
                unit_name varchar NOT NULL,
                unit_code varchar NOT NULL,
                date TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS subjects(
                subject_id serial NOT NULL,
                student integer NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
                unit integer NOT NULL REFERENCES units (unit_id) ON DELETE CASCADE,                                                                                                                                 
                date TIMESTAMP,
                PRIMARY KEY (student, unit)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS exams(
                exam_id serial NOT NULL,
                semester varchar NOT NULL,
                year varchar NOT NULL,
                student integer NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
                unit integer NOT NULL REFERENCES units (unit_id) ON DELETE CASCADE,   
                marks varchar NOT NULL,
                date TIMESTAMP,
                PRIMARY KEY (student, unit)
            )""",
            """
            CREATE TABLE IF NOT EXISTS fees(
                fee_id serial NOT NULL,
                student integer NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
                transaction_type varchar NOT NULL,
                transaction_no varchar NOT NULL,
                description varchar NOT NULL,
                amount varchar NOT NULL,
                date TIMESTAMP,
                PRIMARY KEY (student)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS library(
                book_id serial NOT NULL,
                student integer NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
                title varchar NOT NULL,
                author varchar NOT NULL,
                book_no varchar NOT NULL,
                date TIMESTAMP,
                PRIMARY KEY (student)
            )""",
            """
            CREATE TABLE IF NOT EXISTS hostels(
                hostel_id serial PRIMARY KEY,
                hostel_name varchar NOT NULL,
                rooms varchar NOT NULL,
                hostel_location varchar NOT NULL,
                date TIMESTAMP
            )"""
        ]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return e

    def destroy_table(self):
        """Destroy tables"""
        exams = "DROP TABLE IF EXISTS  exams CASCADE"
        users = "DROP TABLE IF EXISTS  users CASCADE"
        staff = "DROP TABLE IF EXISTS  staff CASCADE"
        accountants = "DROP TABLE IF EXISTS  accountants CASCADE"
        units = "DROP TABLE IF EXISTS units CASCADE"
        subjects = "DROP TABLE IF EXISTS subjects CASCADE"
        fees = "DROP TABLE IF EXISTS fees CASCADE"
        library = "DROP TABLE IF EXISTS library CASCADE"
        units = "DROP TABLE IF EXISTS units CASCADE"
        hostels = "DROP TABLE IF EXISTS hostels CASCADE"
        
        queries = [exams, users, staff, accountants, subjects, fees, library, units, hostels]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return e

    def fetch(self, query):
        """Fetch all query."""
        self.curr.execute(query)
        fetch_all = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return fetch_all
    
    def fetch_one(self, query, var):
        """Fetch one query."""
        self.curr.execute(query, (var,),)
        fetch_one = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return fetch_one


if __name__ == '__main__':
    Database().destroy_table()
    Database().create_table()
