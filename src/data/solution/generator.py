import random
from faker import Faker
from datetime import date
from typing import List, Tuple

from data.solution.model import Department, Project, Person

def generate_people(n: int, male_ratio: float = 0.5, locale: str = "en_US",
                    unique: bool = False, min_age: int = 0, max_age: int = 100) -> List[Person]:
    fake = Faker(locale)
    people = []
    for i in range(n):
        male = random.random() < male_ratio
        generator = fake if not unique else fake.unique
        people.append(Person(
            "O-" + (str(i).zfill(6)),
            generator.name_male() if male else generator.name_female(),
            random.randint(min_age, max_age),
            male))
    return people

def generate_departments(n: int, locale: str = "en_US") -> List[Department]:
    fake = Faker(locale)
    departments = []
    for i in range(n):
        dept_id = f"D-{str(i+1).zfill(3)}"
        name = fake.job() + " Department"
        floor = random.randint(1, 10)
        departments.append(Department(dept_id, name, floor))
    return departments

def generate_projects(n: int, locale: str = "en_US") -> List[Project]:
    fake = Faker(locale)
    projects = []
    statuses = ["Active", "Completed", "Pending"]
    for i in range(n):
        proj_id = f"P-{str(i+1).zfill(3)}"
        name = fake.bs().title()
        budget = random.randint(10000, 1000000)
        deadline = fake.future_date(end_date="+2y")
        status = random.choice(statuses)
        projects.append(Project(proj_id, name, budget, deadline, status))
    return projects

def assign_departments(people: List[Person], departments: List[Department]) -> List[Tuple[str, str, str, int]]:
    """Assigns people to departments (1:N) with job and salary."""
    fake = Faker()
    assignments = []
    for person in people:
        dept = random.choice(departments)
        job = fake.job()
        salary = random.randint(30000, 150000)
        assignments.append((person.id, dept.id, job, salary))
    return assignments

def assign_projects(people: List[Person], projects: List[Project]) -> List[Tuple[str, str]]:
    """Assigns people to projects (N:M)."""
    assignments = []
    for person in people:
        # Each person works on 1 to 3 projects
        num_projects = random.randint(1, 3)
        assigned_projects = random.sample(projects, min(num_projects, len(projects)))
        for proj in assigned_projects:
            assignments.append((person.id, proj.id))
    return assignments
