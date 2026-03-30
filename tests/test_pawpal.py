from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date


def test_mark_complete_changes_status():
    """Task should be marked completed after calling mark_complete()."""
    task = Task(description="Walk", time="08:00", frequency="daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    """Adding a task to a Pet should increase its task count by one."""
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feed", time="07:00", frequency="daily"))
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order should be returned sorted by time."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(description="Evening walk", time="18:00", frequency="daily"))
    pet.add_task(Task(description="Morning walk", time="07:00", frequency="daily"))
    pet.add_task(Task(description="Medication",   time="09:00", frequency="weekly"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_conflict_detection_returns_warning():
    """Two tasks at the same time for the same pet should trigger a warning."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(description="Walk",  time="09:00", frequency="daily"))
    pet.add_task(Task(description="Feed",  time="09:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0
    