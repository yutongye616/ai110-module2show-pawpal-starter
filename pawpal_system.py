from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str                  # format: "HH:MM"
    frequency: str             # "once", "daily", or "weekly"
    completed: bool = False
    due_date: Optional[date] = None

    def mark_complete(self):
        pass

    def is_recurring(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, pet_name: str):
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_tasks(self) -> List[Task]:
        pass

    def sort_by_time(self) -> List[Task]:
        pass

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        pass

    def filter_by_status(self, completed: bool) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[str]:
        pass

    def mark_task_complete(self, task: Task):
        pass

    def generate_next_occurrence(self, task: Task) -> Task:
        pass