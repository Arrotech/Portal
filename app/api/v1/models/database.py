import os

import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import app_config
from utils.serializer import Serializer

config_name = os.getenv("FLASK_ENV")
if config_name is not None:
    DB_URL = app_config[config_name].DB_NAME
else:
    DB_URL = "test_school_portal"


class Database:
    """Initialization."""

    def __init__(self):
        self.db_name = DB_URL
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.conn = psycopg2.connect(
            database=self.db_name, host=self.db_host, user=self.db_user,
            password=self.db_password)
        self.curr = self.conn.cursor(cursor_factory=RealDictCursor)

    def __enter__(self):
        """ Instantitiates and returns the db connection """
        return self.conn

    def __exit__(self, exe_typ, exec_value, exec_tb):
        """ Define what the context manager should do before exit """
        self.conn.close()

    @classmethod
    def create_table(cls):
        """Create tables."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users(
                user_id serial,
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
                created_on TIMESTAMP,
                PRIMARY KEY (admission_no)
            )""",
            """
            CREATE TABLE IF NOT EXISTS institutions(
                institution_id serial,
                institution_name varchar NOT NULL UNIQUE,
                created_on TIMESTAMP,
                PRIMARY KEY (institution_name)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS campuses(
                campus_id serial,
                campus_name varchar NOT NULL,
                campus_location varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (campus_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS certificates(
                certificate_id serial,
                certificate_name varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (certificate_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS departments(
                department_id serial,
                department_name varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (department_name)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS units(
                unit_id serial,
                unit_name varchar NOT NULL UNIQUE,
                unit_code varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (unit_name)
            )""",
            """
            CREATE TABLE IF NOT EXISTS academic_year(
                year_id serial,
                year varchar NOT NULL,
                semester varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (year_id)
            )""",
            """
            CREATE TABLE IF NOT EXISTS hostels(
                hostel_id serial,
                hostel_name varchar NOT NULL UNIQUE,
                rooms varchar NOT NULL,
                gender varchar NOT NULL,
                hostel_location varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (hostel_name)
            )""",
            """
            CREATE TABLE IF NOT EXISTS courses(
                course_id serial,
                course_name varchar UNIQUE,
                department varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (course_id),
                FOREIGN KEY (department) REFERENCES\
                    departments(department_name) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS apply_course(
                application_id serial,
                student varchar NOT NULL,
                institution varchar NOT NULL,
                campus integer NOT NULL,
                certificate integer NOT NULL,
                department varchar NOT NULL,
                course varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (application_id),
                FOREIGN KEY (student) REFERENCES users(admission_no)\
                    ON DELETE CASCADE,
                FOREIGN KEY (institution) REFERENCES\
                    institutions(institution_name) ON DELETE CASCADE,
                FOREIGN KEY (campus) REFERENCES campuses(campus_id)\
                    ON DELETE CASCADE,
                FOREIGN KEY (certificate) REFERENCES\
                    certificates(certificate_id) ON DELETE CASCADE,
                FOREIGN KEY (department) REFERENCES\
                    departments(department_name) ON DELETE CASCADE,
                FOREIGN KEY (course) REFERENCES courses(course_name)\
                    ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS subjects(
                subject_id serial,
                student varchar NOT NULL,
                unit varchar NOT NULL,
                year integer NOT NULL,                                                                                                                                
                created_on TIMESTAMP,
                PRIMARY KEY (subject_id),
                FOREIGN KEY (student) REFERENCES users(admission_no)\
                    ON DELETE CASCADE,
                FOREIGN KEY (unit) REFERENCES units(unit_name)\
                    ON DELETE CASCADE,
                FOREIGN KEY (year) REFERENCES academic_year(year_id)\
                    ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS exams(
                exam_id serial,
                year integer NOT NULL,
                student varchar NOT NULL,
                unit varchar NOT NULL,
                marks integer NOT NULL,
                exam_type varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (exam_id),
                FOREIGN KEY (year) REFERENCES academic_year(year_id)\
                    ON DELETE CASCADE,
                FOREIGN KEY (student) REFERENCES users(admission_no)\
                    ON DELETE CASCADE,
                FOREIGN KEY (unit) REFERENCES units(unit_name)\
                    ON DELETE CASCADE
            )""",
            """
            CREATE TABLE IF NOT EXISTS fees(
                fee_id serial,
                student varchar NOT NULL,
                transaction_type varchar NOT NULL,
                transaction_no varchar NOT NULL,
                description varchar NOT NULL,
                amount varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (fee_id),
                FOREIGN KEY (student) REFERENCES users(admission_no)\
                    ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS library(
                book_id serial UNIQUE,
                student varchar NOT NULL,
                title varchar NOT NULL,
                author varchar NOT NULL,
                book_no varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (book_id),
                FOREIGN KEY (student) REFERENCES users(admission_no)\
                    ON DELETE CASCADE
            )""",
            """
            CREATE TABLE IF NOT EXISTS accommodation(
                accommodation_id serial,
                student varchar NOT NULL,
                hostel varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (accommodation_id),
                FOREIGN KEY (student) REFERENCES users(admission_no)\
                    ON DELETE CASCADE,
                FOREIGN KEY (hostel) REFERENCES hostels(hostel_name)\
                    ON DELETE CASCADE
            )""",
            """
            CREATE TABLE IF NOT EXISTS checklist(
                checklist_id serial,
                student varchar NOT NULL,
                department varchar NOT NULL,
                course varchar NOT NULL,
                certificate integer NOT NULL,
                year integer NOT NULL,
                campus integer NOT NULL,
                hostel varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (checklist_id),
                FOREIGN KEY (student) REFERENCES users(admission_no)\
                    ON DELETE CASCADE,
                FOREIGN KEY (department) REFERENCES\
                    departments(department_name) ON DELETE CASCADE,
                FOREIGN KEY (course) REFERENCES courses(course_name)\
                    ON DELETE CASCADE,
                FOREIGN KEY (certificate) REFERENCES\
                    certificates(certificate_id) ON DELETE CASCADE,
                FOREIGN KEY (year) REFERENCES academic_year(year_id)\
                    ON DELETE CASCADE,
                FOREIGN KEY (campus) REFERENCES campuses(campus_id)\
                    ON DELETE CASCADE,
                FOREIGN KEY (hostel) REFERENCES hostels(hostel_name)\
                    ON DELETE CASCADE
            )""",
            """
            CREATE TABLE IF NOT EXISTS notifications(
                notification_id serial,
                subject varchar NOT NULL,
                description varchar NOT NULL,
                created_on TIMESTAMP,
                PRIMARY KEY (notification_id)
            )"""
        ]
        try:
            with Database() as conn:
                curr = conn.cursor(cursor_factory=RealDictCursor)
                for query in queries:
                    curr.execute(query)
                conn.commit()
            return 'Successfuly created tables'
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    @classmethod
    def destroy_table(cls):
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

        queries = [exams, users, institutions, campuses, certificates,
                   departments, courses, academic_year, apply_course, subjects,
                   fees, library, units, hostels, accommodation, checklist,
                   notifications]
        try:
            with Database() as conn:
                curr = conn.cursor(cursor_factory=RealDictCursor)
                for query in queries:
                    curr.execute(query)
                conn.commit()
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def create_registrar(self):
        """Create default admin."""
        try:
            self.curr.execute(
                ''' INSERT INTO users(firstname, lastname, surname,\
                    admission_no, gender, email, password, role, is_confirmed,\
                    created_on) VALUES('Peter','Gitundu','Kigo','8511024',\
                    'male','registrar@admin.com',\
                    'pbkdf2:sha256:150000$Xlqfm8GS$d8544269c47e1d8f3835d887d3cb\
                    4ba4b939f34584f75db043a374a286558cc9','registrar','false',\
                    'Mon, 14 Dec 2020 00:48:26 GMT') RETURNING firstname,\
                    lastname, surname, admission_no, gender, email, password,\
                    role, is_confirmed, created_on''')
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            Serializer.serialize(f"{e}", 500, "Error")

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
