import os
import json

import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import app_config
from utils.serializer import Serializer


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
                admission_no varchar NOT NULL UNIQUE,
                gender varchar NOT NULL,
                email varchar NOT NULL,
                password varchar NOT NULL,
                role varchar NOT NULL,
                is_confirmed BOOLEAN DEFAULT False,
                confirmed_on TIMESTAMP,
                created_on TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS institutions(
                institution_id serial PRIMARY KEY,
                institution_name varchar NOT NULL UNIQUE,
                created_on TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS campuses(
                campus_id serial PRIMARY KEY,
                campus_name varchar NOT NULL,
                campus_location varchar NOT NULL,
                created_on TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS certificates(
                certificate_id serial PRIMARY KEY,
                certificate_name varchar NOT NULL,
                created_on TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS departments(
                department_id serial PRIMARY KEY,
                department_name varchar NOT NULL UNIQUE,
                created_on TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS courses(
                course_id serial NOT NULL,
                course_name varchar UNIQUE,
                department varchar NOT NULL REFERENCES departments (department_name) ON DELETE CASCADE,
                created_on TIMESTAMP,
                PRIMARY KEY (department)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS academic_year(
                year_id serial UNIQUE,
                year varchar NOT NULL,
                semester varchar NOT NULL,
                created_on TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS apply_course(
                application_id serial UNIQUE,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                institution varchar NOT NULL REFERENCES institutions (institution_name) ON DELETE CASCADE,
                campus integer NOT NULL REFERENCES campuses (campus_id) ON DELETE CASCADE,
                certificate integer NOT NULL REFERENCES certificates (certificate_id) ON DELETE CASCADE,
                department varchar NOT NULL REFERENCES departments (department_name) ON DELETE CASCADE,
                course varchar NOT NULL REFERENCES courses (course_name) ON DELETE CASCADE,
                created_on TIMESTAMP,
                PRIMARY KEY (student, institution, campus, certificate, department, course)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS units(
                unit_id serial PRIMARY KEY,
                unit_name varchar NOT NULL UNIQUE,
                unit_code varchar NOT NULL,
                created_on TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS subjects(
                subject_id serial UNIQUE,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                unit varchar NOT NULL REFERENCES units (unit_name) ON DELETE CASCADE,                                                                                                                                 
                created_on TIMESTAMP,
                PRIMARY KEY (student, unit)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS exams(
                exam_id serial UNIQUE,
                year integer NOT NULL REFERENCES academic_year (year_id) ON DELETE CASCADE,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                unit varchar NOT NULL REFERENCES units (unit_name) ON DELETE CASCADE,   
                marks varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (year, student, unit)
            )""",
            """
            CREATE TABLE IF NOT EXISTS fees(
                fee_id serial UNIQUE,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                transaction_type varchar NOT NULL,
                transaction_no varchar NOT NULL,
                description varchar NOT NULL,
                amount varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (student)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS library(
                book_id serial UNIQUE,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                title varchar NOT NULL,
                author varchar NOT NULL,
                book_no varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (student)
            )""",
            """
            CREATE TABLE IF NOT EXISTS hostels(
                hostel_id serial PRIMARY KEY,
                hostel_name varchar NOT NULL UNIQUE,
                rooms varchar NOT NULL,
                gender varchar NOT NULL,
                hostel_location varchar NOT NULL,
                created_on TIMESTAMP
            )""",
            """
            CREATE TABLE IF NOT EXISTS accommodation(
                accommodation_id serial UNIQUE,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                hostel varchar NOT NULL REFERENCES hostels (hostel_name) ON DELETE CASCADE,
                created_on TIMESTAMP,
                PRIMARY KEY (student, hostel)
            )""",
            """
            CREATE TABLE IF NOT EXISTS checklist(
                checklist_id serial UNIQUE,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                department varchar NOT NULL REFERENCES departments (department_name) ON DELETE CASCADE,
                course varchar NOT NULL REFERENCES courses (course_name) ON DELETE CASCADE,
                certificate integer NOT NULL REFERENCES certificates (certificate_id) ON DELETE CASCADE,
                year integer NOT NULL REFERENCES academic_year (year_id) ON DELETE CASCADE,
                campus integer NOT NULL REFERENCES campuses (campus_id) ON DELETE CASCADE,
                hostel varchar NOT NULL REFERENCES hostels (hostel_name) ON DELETE CASCADE,
                created_on TIMESTAMP,
                PRIMARY KEY (student, department, course, certificate, year, campus, hostel)
            )""",
            """
            CREATE TABLE IF NOT EXISTS notifications(
                notification_id serial PRIMARY KEY,
                subject varchar NOT NULL,
                description varchar NOT NULL,
                created_on TIMESTAMP
            )"""
        ]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def destroy_table(self):
        """Destroy tables"""
        exams = "DROP TABLE IF EXISTS  exams CASCADE"
        users = "DROP TABLE IF EXISTS  users CASCADE"
        institutions = "DROP TABLE IF EXISTS institutions CASCADE"
        campuses = "DROP TABLE IF EXISTS campuses CASCADE"
        certificates = "DROP TABLE IF EXISTS certificates CASCADE"
        departments = "DROP TABLE IF EXISTS departments CASCADE"
        courses = "DROP TABLE IF EXISTS courses CASCADE"
        academic_year = "DROP TABLE IF EXISTS academic_year CASCADE"
        apply_course = "DROP TABLE IF EXISTS apply_course CASCADE"
        units = "DROP TABLE IF EXISTS units CASCADE"
        subjects = "DROP TABLE IF EXISTS subjects CASCADE"
        fees = "DROP TABLE IF EXISTS fees CASCADE"
        library = "DROP TABLE IF EXISTS library CASCADE"
        units = "DROP TABLE IF EXISTS units CASCADE"
        hostels = "DROP TABLE IF EXISTS hostels CASCADE"
        accommodation = "DROP TABLE IF EXISTS accommodation CASCADE"
        checklist = "DROP TABLE IF EXISTS checklist CASCADE"
        notifications = "DROP TABLE IF EXISTS notifications CASCADE"

        queries = [exams, users, institutions, campuses, certificates, departments,
                   courses, academic_year, apply_course, subjects, fees, library, units, hostels, accommodation, checklist, notifications]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    # def create_registrar(self):
    #     """Create default admin."""
    #     try:
    #         self.curr.execute(
    #             ''' INSERT INTO users(firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed,  created_on)\
    #                 VALUES('Peter','Gitundu','Kigo','8511024','male','petergitundu44@gmail.com','pbkdf2:sha256:150000$Xlqfm8GS$d8544269c47e1d8f3835d887d3cb4ba4b939f34584f75db043a374a286558cc9','registrar','false','Mon, 14 Dec 2020 00:48:26 GMT') RETURNING firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed, created_on''')
    #         response = self.curr.fetchone()
    #         self.conn.commit()
    #         self.curr.close()
    #         return response
    #     except Exception as e:
    #         Serializer.serialize(f"{e}", 500, "Error")

    def fetch(self, query):
        """Fetch all query."""
        try:
            self.curr.execute(query)
            fetch_all = self.curr.fetchall()
            self.conn.commit()
            self.curr.close()
            return fetch_all
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def fetch_group(self, query, var, *args, **kwargs):
        """Fetch one query."""
        try:
            self.curr.execute(query, (var,),)
            fetch_group = self.curr.fetchall()
            self.conn.commit()
            self.curr.close()
            return fetch_group
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def fetch_one(self, query, var):
        """Fetch one query."""
        try:
            self.curr.execute(query, (var,),)
            fetch_one = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return fetch_one
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")


if __name__ == '__main__':
    Database().destroy_table()
    Database().create_table()
