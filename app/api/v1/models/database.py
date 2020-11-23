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
            CREATE TABLE IF NOT EXISTS staff(
                staff_id serial PRIMARY KEY,
                firstname varchar NOT NULL,
                lastname varchar NOT NULL,
                username varchar NOT NULL,
                email varchar NOT NULL,
                password varchar NOT NULL,
                role varchar NOT NULL,
                created_on TIMESTAMP
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
                semester varchar NOT NULL,
                year varchar NOT NULL,
                student varchar NOT NULL REFERENCES users (admission_no) ON DELETE CASCADE,
                unit varchar NOT NULL REFERENCES units (unit_name) ON DELETE CASCADE,   
                marks varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (student, unit)
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
                hostel varchar NOT NULL REFERENCES hostels (hostel_name) ON DELETE CASCADE,
                created_on TIMESTAMP,
                PRIMARY KEY (student, department, course, hostel)
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
            return e

    def destroy_table(self):
        """Destroy tables"""
        exams = "DROP TABLE IF EXISTS  exams CASCADE"
        users = "DROP TABLE IF EXISTS  users CASCADE"
        staff = "DROP TABLE IF EXISTS  staff CASCADE"
        accountants = "DROP TABLE IF EXISTS  accountants CASCADE"
        institutions = "DROP TABLE IF EXISTS institutions CASCADE"
        campuses = "DROP TABLE IF EXISTS campuses CASCADE"
        certificates = "DROP TABLE IF EXISTS certificates CASCADE"
        departments = "DROP TABLE IF EXISTS departments CASCADE"
        courses = "DROP TABLE IF EXISTS courses CASCADE"
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

        queries = [exams, users, staff, accountants, institutions, campuses, certificates, departments,
                   courses, apply_course, subjects, fees, library, units, hostels, accommodation, checklist, notifications]
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
