from dataclasses import dataclass, field
from typing import List
from datetime import date

@dataclass
class Person:
    id: str
    name: str
    age: int
    male: bool = True

    def __str__(self) -> str:
        return f"#{self.id}: {self.name} ({self.age}, {self.male})"

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

@dataclass
class Department:
    id: str
    name: str
    floor: int

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id}, Floor: {self.floor})"

    def __hash__(self) -> int:
        return hash(self.id)

@dataclass
class Project:
    id: str
    name: str
    budget: int
    deadline: date
    status: str # New field: Active, Completed, Pending

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id}, Budget: {self.budget}, Deadline: {self.deadline}, Status: {self.status})"

    def __hash__(self) -> int:
        return hash(self.id)
