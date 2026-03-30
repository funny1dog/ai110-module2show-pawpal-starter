from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup pets ---
mochi = Pet(name="Mochi", species="dog", special_needs=["joint supplement"])
luna = Pet(name="Luna", species="cat")

# --- Setup owner ---
# Budget is 30 min — tight enough that LOW tasks get dropped when HIGH tasks consume the budget first
jordan = Owner(name="Jordan", available_minutes=30, pets=[mochi, luna])

# --- Tasks across different priorities AND time slots ---
# Key demo: a HIGH evening task should appear before a LOW morning task
# because priority is now the primary sort key.

grooming = Task(
    title="Brushing", duration_minutes=20, priority="medium",
    category="grooming", frequency="weekly", time_slot="evening",
    last_done=date.today()  # done today → skipped as not due
)
enrichment = Task(
    title="Toy Enrichment", duration_minutes=15, priority="low",
    category="enrichment", time_slot="morning"   # LOW + morning
)
medication = Task(
    title="Joint Supplement", duration_minutes=5, priority="medium",
    category="health", time_slot="afternoon"      # MEDIUM + afternoon (boosted to HIGH by special_needs)
)
feeding = Task(
    title="Feeding", duration_minutes=10, priority="high",
    category="nutrition", frequency="daily", time_slot="morning"  # HIGH + morning
)
evening_walk = Task(
    title="Evening Walk", duration_minutes=20, priority="high",
    category="exercise", time_slot="evening"      # HIGH + evening → must appear before LOW morning
)

mochi.add_task(grooming)
mochi.add_task(medication)
mochi.add_task(evening_walk)
luna.add_task(enrichment)
luna.add_task(feeding)

# --- Build scheduler ---
scheduler = Scheduler(owner=jordan)
for task in jordan.all_tasks():
    scheduler.add_task(task)

# --- 1. Priority-first vs time-first comparison ---
print("=== sort_by_time() — time slot is primary key ===")
for t in scheduler.sort_by_time():
    print(f"  [{t.time_slot:9}] [{t.priority:6}] {t.title} ({t.pet_name})")

print()
print("=== generate_plan() scheduling queue — priority is primary key ===")
print("  HIGH tasks enter the greedy loop first, regardless of time slot.")
print("  LOW/MEDIUM tasks only get budget if HIGH tasks leave room.")
print("  (budget is 30 min — Evening Walk HIGH 20min + Joint Supplement boosted-HIGH 5min = 25min fits;")
print("   Toy Enrichment LOW 15min is attempted last and gets cut if budget runs out)")

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
