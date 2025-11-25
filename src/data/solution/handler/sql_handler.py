import oracledb
import os
from typing import List, Tuple
from datetime import date
from dotenv import load_dotenv

from data.solution.model import Department, Project, Person

# Load environment variables from .env file
load_dotenv()

# Connection details from environment variables
DB_HOST = os.getenv("DB_HOST", "codd.inf.unideb.hu")
DB_PORT = int(os.getenv("DB_PORT", "1521"))
DB_SERVICE = os.getenv("DB_SERVICE", "ora21cp.inf.unideb.hu")
DB_USER = os.getenv("DB_USER")  # No default for security
DB_PASS = os.getenv("DB_PASS")  # No default for security

def get_connection(user=DB_USER, password=DB_PASS):
    dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
    return oracledb.connect(user=user, password=password, dsn=dsn)

def create_tables(conn):
    cursor = conn.cursor()
    
    # Drop tables if they exist (reverse order of dependencies)
    tables = ["A_PERSON_PROJECT", "A_PERSON_DEPARTMENT", "A_PROJECT", "A_DEPARTMENT", "A_PERSON"]
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE {table}")
            print(f"Dropped table {table}")
        except oracledb.DatabaseError:
            pass # Table didn't exist

    # Create PERSON table
    cursor.execute("""
        CREATE TABLE A_PERSON (
            id VARCHAR2(50) PRIMARY KEY,
            name VARCHAR2(100),
            age NUMBER,
            male NUMBER(1)
        )
    """)

    # Create DEPARTMENT table
    cursor.execute("""
        CREATE TABLE A_DEPARTMENT (
            id VARCHAR2(50) PRIMARY KEY,
            name VARCHAR2(100),
            floor NUMBER
        )
    """)

    # Create PROJECT table
    cursor.execute("""
        CREATE TABLE A_PROJECT (
            id VARCHAR2(50) PRIMARY KEY,
            name VARCHAR2(100),
            budget NUMBER,
            deadline DATE,
            status VARCHAR2(20)
        )
    """)

    # Create PERSON_DEPARTMENT table (1:N)
    cursor.execute("""
        CREATE TABLE A_PERSON_DEPARTMENT (
            person_id VARCHAR2(50),
            department_id VARCHAR2(50),
            job VARCHAR2(100),
            salary NUMBER,
            PRIMARY KEY (person_id),
            FOREIGN KEY (person_id) REFERENCES A_PERSON(id),
            FOREIGN KEY (department_id) REFERENCES A_DEPARTMENT(id)
        )
    """)

    # Create PERSON_PROJECT table (N:M)
    cursor.execute("""
        CREATE TABLE A_PERSON_PROJECT (
            person_id VARCHAR2(50),
            project_id VARCHAR2(50),
            PRIMARY KEY (person_id, project_id),
            FOREIGN KEY (person_id) REFERENCES A_PERSON(id),
            FOREIGN KEY (project_id) REFERENCES A_PROJECT(id)
        )
    """)
    
    print("Tables created successfully.")
    cursor.close()

def insert_data(conn, people: List[Person], departments: List[Department], projects: List[Project], 
                dept_assignments: List[Tuple[str, str, str, int]], proj_assignments: List[Tuple[str, str]]):
    cursor = conn.cursor()

    # Insert People
    data_people = [(p.id, p.name, p.age, 1 if p.male else 0) for p in people]
    cursor.executemany("INSERT INTO A_PERSON (id, name, age, male) VALUES (:1, :2, :3, :4)", data_people)

    # Insert Departments
    data_depts = [(d.id, d.name, d.floor) for d in departments]
    cursor.executemany("INSERT INTO A_DEPARTMENT (id, name, floor) VALUES (:1, :2, :3)", data_depts)

    # Insert Projects
    data_projs = [(p.id, p.name, p.budget, p.deadline, p.status) for p in projects]
    cursor.executemany("INSERT INTO A_PROJECT (id, name, budget, deadline, status) VALUES (:1, :2, :3, :4, :5)", data_projs)

    # Insert Assignments
    cursor.executemany("INSERT INTO A_PERSON_DEPARTMENT (person_id, department_id, job, salary) VALUES (:1, :2, :3, :4)", dept_assignments)
    cursor.executemany("INSERT INTO A_PERSON_PROJECT (person_id, project_id) VALUES (:1, :2)", proj_assignments)

    conn.commit()
    print("Data inserted successfully.")
    cursor.close()

def read_data(conn):
    cursor = conn.cursor()
    
    # Read People
    cursor.execute("SELECT id, name, age, male FROM A_PERSON")
    people = [Person(row[0], row[1], row[2], bool(row[3])) for row in cursor]
    
    # Read Departments
    cursor.execute("SELECT id, name, floor FROM A_DEPARTMENT")
    departments = [Department(row[0], row[1], row[2]) for row in cursor]
    
    # Read Projects
    cursor.execute("SELECT id, name, budget, deadline, status FROM A_PROJECT")
    projects = []
    for row in cursor:
        # Oracle returns datetime, we need date
        d = row[3]
        if hasattr(d, 'date'): d = d.date()
        projects.append(Project(row[0], row[1], row[2], d, row[4]))

    print(f"Read {len(people)} people, {len(departments)} departments, {len(projects)} projects from DB.")
    cursor.close()
    return people, departments, projects
