from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# --- Setup ---
owner = Owner(name="Alex", email="alex@email.com")

dog = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
cat = Pet(name="Mochi", species="Cat", breed="Siamese", age=2)

# Tasks added OUT OF ORDER to test sorting
dog.add_task(Task(description="Evening walk",    time="18:00", frequency="daily",  due_date=date.today()))
dog.add_task(Task(description="Flea medication", time="09:00", frequency="weekly", due_date=date.today()))
dog.add_task(Task(description="Morning walk",    time="07:00", frequency="daily",  due_date=date.today()))

cat.add_task(Task(description="Vet appointment", time="14:00", frequency="once",  due_date=date.today()))
cat.add_task(Task(description="Feed breakfast",  time="08:00", frequency="daily", due_date=date.today()))

# Intentional conflict for Buddy
dog.add_task(Task(description="Bath time", time="09:00", frequency="once", due_date=date.today()))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)

# --- 1. Sorting ---
print("=" * 50)
print("  1. SORTED SCHEDULE (chronological)")
print("=" * 50)
for t in scheduler.sort_by_time():
    print(f"  {t.time}  {t.description} ({t.frequency})")

# --- 2. Filtering by status ---
print("\n" + "=" * 50)
print("  2. FILTER — incomplete tasks only")
print("=" * 50)
for t in scheduler.filter_by_status(completed=False):
    print(f"  ○ {t.description}")

# --- 3. Filtering by pet ---
print("\n" + "=" * 50)
print("  3. FILTER — Buddy's tasks only")
print("=" * 50)
for t in scheduler.filter_by_pet("Buddy"):
    print(f"  {t.time}  {t.description}")

# --- 4. Conflict detection ---
print("\n" + "=" * 50)
print("  4. CONFLICT DETECTION")
print("=" * 50)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(f"  ⚠️  {c}")
else:
    print("  ✅ No conflicts found.")

# --- 5. Recurring task ---
print("\n" + "=" * 50)
print("  5. RECURRING TASK — mark complete & regenerate")
print("=" * 50)
morning_walk = dog.tasks[2]
print(f"  Before: '{morning_walk.description}' completed={morning_walk.completed}")
next_task = scheduler.mark_task_complete(morning_walk)
print(f"  After:  '{morning_walk.description}' completed={morning_walk.completed}")
if next_task:
    print(f"  Next occurrence created for: {next_task.due_date}")

print("=" * 50)