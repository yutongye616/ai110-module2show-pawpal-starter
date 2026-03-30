from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# --- Setup ---
owner = Owner(name="Alex", email="alex@email.com")

dog = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
cat = Pet(name="Mochi", species="Cat", breed="Siamese", age=2)

# --- Add tasks (intentionally out of order to test sorting) ---
dog.add_task(Task(description="Morning walk",    time="07:00", frequency="daily",  due_date=date.today()))
dog.add_task(Task(description="Evening walk",    time="18:00", frequency="daily",  due_date=date.today()))
dog.add_task(Task(description="Flea medication", time="09:00", frequency="weekly", due_date=date.today()))

cat.add_task(Task(description="Feed breakfast",  time="08:00", frequency="daily",  due_date=date.today()))
cat.add_task(Task(description="Vet appointment", time="14:00", frequency="once",   due_date=date.today()))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)

# --- Print today's schedule ---
print("=" * 45)
print("       🐾  PawPal+ — Today's Schedule")
print("=" * 45)

sorted_tasks = scheduler.sort_by_time()
for pet in owner.pets:
    pet_tasks = [t for t in sorted_tasks if t in pet.get_tasks()]
    if pet_tasks:
        print(f"\n  {pet.name} ({pet.species})")
        print(f"  {'-' * 30}")
        for task in pet_tasks:
            status = "✓" if task.completed else "○"
            print(f"  [{status}] {task.time}  —  {task.description}  ({task.frequency})")

# --- Conflict check ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n  ⚠️  Conflicts detected:")
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("\n  ✅  No scheduling conflicts.")

print("=" * 45)