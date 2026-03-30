from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str
    frequency: str
    completed: bool = False
    due_date: Optional[date] = None

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Return True if this task repeats daily or weekly."""
        return self.frequency in ("daily", "weekly")


@dataclass
class Pet:
    """Stores a pet's details and their list of tasks."""
    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str, email: str):
        """Initialize an Owner with a name, email, and empty pet list."""
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove a pet by name from this owner's collection."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The brain of PawPal+: retrieves, organizes, and manages tasks."""

    def __init__(self, owner: Owner):
        """Initialize the Scheduler with an Owner instance."""
        self.owner = owner

    def get_todays_tasks(self) -> List[Task]:
        """Return all incomplete tasks for today."""
        return [t for t in self.owner.get_all_tasks() if not t.completed]

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted chronologically by HH:MM time."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to a specific pet by name."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for tasks scheduled at the same time."""
        warnings = []
        for pet in self.owner.pets:
            seen_times = {}
            for task in pet.get_tasks():
                if task.time in seen_times:
                    warnings.append(
                        f"Conflict for {pet.name}: '{task.description}' and "
                        f"'{seen_times[task.time]}' are both scheduled at {task.time}"
                    )
                else:
                    seen_times[task.time] = task.description
        return warnings

    def mark_task_complete(self, task: Task):
        """Mark a task complete and generate next occurrence if recurring."""
        task.mark_complete()
        if task.is_recurring():
            return self.generate_next_occurrence(task)
        return None

    def generate_next_occurrence(self, task: Task) -> Task:
        """Create a new Task for the next occurrence of a recurring task."""
        delta = timedelta(days=1) if task.frequency == "daily" else timedelta(weeks=1)
        next_date = (task.due_date or date.today()) + delta
        return Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            completed=False,
            due_date=next_date
        )
