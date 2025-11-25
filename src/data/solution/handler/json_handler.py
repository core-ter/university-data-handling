import json
import os
from typing import List
from datetime import date

from data.solution.model import Department, Project

def write_departments(departments: List[Department], path: str, file_name: str = "departments.json", pretty: bool = True) -> None:
    with open(os.path.join(path, file_name), "w", encoding="utf-8") as file:
        json.dump(
            [dept.__dict__ for dept in departments],
            file,
            indent=2 if pretty else None
        )

def read_departments(path: str, file_name: str = "departments.json") -> List[Department]:
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        data = json.load(file)
        return [Department(**d) for d in data]

def write_projects(projects: List[Project], path: str, file_name: str = "projects.json", pretty: bool = True) -> None:
    with open(os.path.join(path, file_name), "w", encoding="utf-8") as file:
        data = []
        for proj in projects:
            d = proj.__dict__.copy()
            d["deadline"] = proj.deadline.isoformat()
            data.append(d)
        json.dump(data, file, indent=2 if pretty else None)

def read_projects(path: str, file_name: str = "projects.json") -> List[Project]:
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        data = json.load(file)
        projects = []
        for d in data:
            d["deadline"] = date.fromisoformat(d["deadline"])
            projects.append(Project(**d))
        return projects
