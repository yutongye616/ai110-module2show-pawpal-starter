from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, timedelta


# --- Happy path tests ---

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
    """Tasks added out of order should be returned sorted by HH:MM."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(description="Evening walk", time="18:00", frequency="daily"))
    pet.add_task(Task(description="Morning walk", time="07:00", frequency="daily"))
    pet.add_task(Task(description="Medication",   time="09:00", frequency="weekly"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    times = [t.time for t in scheduler.sort_by_time()]
    assert times == sorted(times)


def test_conflict_detection_returns_warning():
    """Two tasks at the same time for the same pet should trigger a warning."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(description="Walk", time="09:00", frequency="daily"))
    pet.add_task(Task(description="Feed", time="09:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0


def test_recurrence_creates_next_day_task():
    """Marking a daily task complete should generate a new task for tomorrow."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog")
    today = date.today()
    task = Task(description="Walk", time="07:00", frequency="daily", due_date=today)
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task)
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


# --- Edge case tests ---

def test_pet_with_no_tasks_returns_empty_list():
    """A pet with no tasks should return an empty list without crashing."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Mochi", species="Cat")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []


def test_filter_by_pet_returns_correct_tasks():
    """filter_by_pet should return only that pet's tasks."""
    owner = Owner(name="Alex", email="alex@email.com")
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Mochi", species="Cat")
    dog.add_task(Task(description="Walk", time="07:00", frequency="daily"))
    cat.add_task(Task(description="Feed", time="08:00", frequency="daily"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)
    buddy_tasks = scheduler.filter_by_pet("Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].description == "Walk"


def test_filter_by_status_returns_incomplete_only():
    """filter_by_status(False) should return only incomplete tasks."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog")
    t1 = Task(description="Walk", time="07:00", frequency="daily")
    t2 = Task(description="Feed", time="08:00", frequency="daily")
    t1.mark_complete()
    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    incomplete = scheduler.filter_by_status(completed=False)
    assert len(incomplete) == 1
    assert incomplete[0].description == "Feed"


def test_once_task_does_not_recur():
    """Marking a one-time task complete should not generate a next occurrence."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog")
    task = Task(description="Vet visit", time="10:00", frequency="once", due_date=date.today())
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task)
    assert next_task is None