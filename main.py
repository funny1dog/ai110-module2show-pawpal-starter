from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup pets ---
mochi = Pet(name="Mochi", species="dog", special_needs=["joint supplement"])
luna = Pet(name="Luna", species="cat")

# --- Setup owner ---
jordan = Owner(name="Jordan", available_minutes=120, pets=[mochi, luna])

# --- Add tasks OUT OF ORDER (evening → afternoon → morning) to show sorting ---
grooming = Task(
    title="Brushing", duration_minutes=20, priority="medium",
    category="grooming", frequency="weekly", time_slot="evening",
    last_done=date.today()  # done today → skipped as not due
)
enrichment = Task(
    title="Toy Enrichment", duration_minutes=15, priority="low",
    category="enrichment", time_slot="afternoon"
)
medication = Task(
    title="Joint Supplement", duration_minutes=5, priority="medium",
    category="health", time_slot="morning"
)
feeding = Task(
    title="Feeding", duration_minutes=10, priority="high",
    category="nutrition", frequency="daily", time_slot="morning"
)
morning_walk = Task(
    title="Morning Walk", duration_minutes=30, priority="high",
    category="exercise", time_slot="morning"
)

# Add to pets (also out of order)
mochi.add_task(grooming)
mochi.add_task(medication)
mochi.add_task(morning_walk)
luna.add_task(enrichment)
luna.add_task(feeding)

# --- Intentional conflicts for demo ---
# Same-pet conflict: Mochi gets a second morning task alongside Morning Walk
mochi_bath = Task(
    title="Bath Time", duration_minutes=15, priority="medium",
    category="grooming", time_slot="morning"  # same slot as Morning Walk → same-pet conflict
)
mochi.add_task(mochi_bath)

# Cross-pet conflict: Luna also gets a morning task → owner can't do both pets at once
luna_checkup = Task(
    title="Health Checkup", duration_minutes=10, priority="high",
    category="health", time_slot="morning"  # same slot as Mochi's tasks → cross-pet conflict
)
luna.add_task(luna_checkup)

# --- Build scheduler ---
scheduler = Scheduler(owner=jordan)
for task in jordan.all_tasks():
    scheduler.add_task(task)

# --- 1. sort_by_time(): show tasks as added vs after sorting ---
print("=== Tasks as added (original order) ===")
for t in scheduler.tasks:
    print(f"  [{t.time_slot:9}] {t.title} ({t.pet_name})")

print()
print("=== After sort_by_time() ===")
for t in scheduler.sort_by_time():
    print(f"  [{t.time_slot:9}] {t.title} ({t.pet_name})")

print()

# --- 2. filter_tasks() examples ---
print("=== filter: Mochi's tasks only ===")
for t in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {t.title} [{t.time_slot}]")

print()
print("=== filter: incomplete tasks only ===")
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.title} — completed: {t.completed}")

print()
print("=== filter: Mochi's incomplete tasks ===")
for t in scheduler.filter_tasks(pet_name="Mochi", completed=False):
    print(f"  {t.title} [{t.time_slot}] — due today: {t.is_due_today()}")

print()

# --- 3. complete_task(): mark a recurring task done and auto-create next occurrence ---
print("=== complete_task() demo ===")
print(f"  Before: {[t.title for t in scheduler.tasks]}")

next_feeding = scheduler.complete_task("Feeding")
print(f"  After completing 'Feeding' (daily):")
print(f"    Next occurrence created: {next_feeding.title} | completed={next_feeding.completed} | last_done={next_feeding.last_done} | next_due={next_feeding.next_due}")
print(f"    is_due_today() → {next_feeding.is_due_today()}  (False — due tomorrow via timedelta(days=1))")
print(f"  Pool titles: {[t.title for t in scheduler.tasks]}")

print()

# --- 4. Full plan ---
plan = scheduler.generate_plan()
print(plan.display())
