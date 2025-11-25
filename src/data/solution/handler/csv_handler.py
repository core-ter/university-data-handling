import csv
import os
from typing import List, Tuple
from datetime import date

from data.solution.model import Department, Project, Person

def read_people(path: str, file_name: str = "people.csv", delimiter: str = ";") -> List[Person]:
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return [Person(row["id"], row["name"], int(row["age"]), row["male"] == "True") for row in reader]

def write_people(people: List[Person], path: str, file_name: str = "people.csv", delimiter: str = ";") -> None:
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "age", "male"], delimiter=delimiter)
        writer.writeheader()
        for person in people:
            writer.writerow(person.__dict__)

def read_departments(path: str, file_name: str = "departments.csv", delimiter: str = ";") -> List[Department]:
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return [Department(row["id"], row["name"], int(row["floor"])) for row in reader]

def write_departments(departments: List[Department], path: str, file_name: str = "departments.csv", delimiter: str = ";") -> None:
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "floor"], delimiter=delimiter)
        writer.writeheader()
        for dept in departments:
            writer.writerow(dept.__dict__)

def write_projects(projects: List[Project], path: str, file_name: str = "projects.csv", delimiter: str = ";") -> None:
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "budget", "deadline", "status"], delimiter=delimiter)
        writer.writeheader()
        for proj in projects:
            row = proj.__dict__.copy()
            row["deadline"] = proj.deadline.isoformat()
            writer.writerow(row)

def read_projects(path: str, file_name: str = "projects.csv", delimiter: str = ";") -> List[Project]:
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return [Project(row["id"], row["name"], int(row["budget"]), date.fromisoformat(row["deadline"]), row["status"]) for row in reader]

def write_dept_assignments(assignments: List[Tuple[str, str, str, int]], path: str, file_name: str = "dept_assignments.csv", delimiter: str = ";") -> None:
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["person_id", "department_id", "job", "salary"])
        writer.writerows(assignments)

def read_dept_assignments(path: str, file_name: str = "dept_assignments.csv", delimiter: str = ";") -> List[Tuple[str, str, str, int]]:
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader) # Skip header
        return [(row[0], row[1], row[2], int(row[3])) for row in reader]

def write_proj_assignments(assignments: List[Tuple[str, str]], path: str, file_name: str = "proj_assignments.csv", delimiter: str = ";") -> None:
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["person_id", "project_id"])
        writer.writerows(assignments)

def read_proj_assignments(path: str, file_name: str = "proj_assignments.csv", delimiter: str = ";") -> List[Tuple[str, str]]:
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader) # Skip header
        return [(row[0], row[1]) for row in reader]
