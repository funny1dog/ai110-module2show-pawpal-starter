from datetime import date
from tabulate import tabulate
from pawpal_system import Owner, Pet, Task, Scheduler

# ---------------------------------------------------------------------------
# Emoji maps for CLI output
# ---------------------------------------------------------------------------
CATEGORY_EMOJI = {
    "health":      "💊",
    "nutrition":   "🍖",
    "exercise":    "🏃",
    "grooming":    "✂️ ",
    "enrichment":  "🧸",
    "other":       "📋",
}
PRIORITY_EMOJI = {
    "high":   "🔴",
    "medium": "🟡",
    "low":    "🟢",
}
SLOT_EMOJI = {
    "morning":   "🌅",
    "afternoon": "☀️ ",
    "evening":   "🌙",
    "any":       "🔄",
}


def task_table(tasks, title=None):
    """Return a tabulate-formatted string for a list of Task objects."""
    rows = []
    for t in tasks:
        rows.append([
            f"{SLOT_EMOJI.get(t.time_slot, '')} {t.time_slot}",
            f"{PRIORITY_EMOJI.get(t.priority, '')} {t.priority}",
            f"{CATEGORY_EMOJI.get(t.category, '📋')} {t.title}",
            t.pet_name or "—",
            f"{t.duration_minutes} min",
            "✅" if t.completed else "⬜",
        ])
    header = ["Slot", "Priority", "Task", "Pet", "Duration", "Done"]
    table = tabulate(rows, headers=header, tablefmt="rounded_outline")
    if title:
        return f"\n{title}\n{table}"
    return table


# --- Setup pets ---
mochi = Pet(name="Mochi", species="dog", special_needs=["joint supplement"])
luna = Pet(name="Luna", species="cat")

# --- Setup owner ---
# Budget is 30 min — tight enough that LOW tasks get dropped when HIGH tasks consume the budget first
jordan = Owner(name="Jordan", available_minutes=30, pets=[mochi, luna])

# --- Tasks across different priorities AND time slots ---
# Key demo: a HIGH evening task should appear before a LOW morning task
# because priority is now the primary sort key in generate_plan().

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

# --- 1. sort_by_time(): time slot is the primary key ---
print(task_table(scheduler.sort_by_time(),
                 title="=== sort_by_time() — time slot is primary key ==="))

# --- 2. filter_tasks() examples ---
print(task_table(scheduler.filter_tasks(pet_name="Mochi"),
                 title="=== filter: Mochi's tasks only ==="))

print(task_table(scheduler.filter_tasks(completed=False),
                 title="=== filter: incomplete tasks only ==="))

print(task_table(scheduler.filter_tasks(pet_name="Mochi", completed=False),
                 title="=== filter: Mochi's incomplete tasks ==="))

# --- 3. complete_task(): mark a recurring task done and auto-create next occurrence ---
print("\n=== complete_task() demo ===")
print(f"  Pool before: {[t.title for t in scheduler.tasks]}")
next_feeding = scheduler.complete_task("Feeding")
print(f"  Completed 'Feeding' (daily) →")
print(f"    Next occurrence: {next_feeding.title} | completed={next_feeding.completed} "
      f"| last_done={next_feeding.last_done} | next_due={next_feeding.next_due}")
print(f"    is_due_today() → {next_feeding.is_due_today()}  (False — due tomorrow)")
print(f"  Pool after:  {[t.title for t in scheduler.tasks]}")

# --- 4. Full plan ---
plan = scheduler.generate_plan()

print(f"\n{'='*60}")
print(f"  {jordan.name}'s Daily Plan")
print(f"  Budget: {plan.total_minutes} / {jordan.available_minutes} min used")
effort = plan.effort_score()
LABEL_EMOJI = {"Light": "🟢", "Moderate": "🟡", "Demanding": "🟠", "Heavy": "🔴"}
print(f"  Day Load: {LABEL_EMOJI[effort['label']]} {effort['label']}  "
      f"| Score: {effort['score']}/100  "
      f"| Time util: {effort['breakdown']['time_utilization']} pts  "
      f"| Priority wt: {effort['breakdown']['priority_weight']} pts")
print(f"{'='*60}")

# Scheduled tasks grouped by time slot
slots = ["morning", "afternoon", "evening", "any"]
slot_labels = {"morning": "🌅 Morning", "afternoon": "☀️  Afternoon",
               "evening": "🌙 Evening", "any": "🔄 Unslotted"}
for slot in slots:
    slot_tasks = [t for t in plan.scheduled_tasks if t.time_slot == slot]
    if slot_tasks:
        print(task_table(slot_tasks, title=slot_labels[slot]))

if plan.skipped_recurring:
    print(f"\n⏭  Skipped — not due today ({len(plan.skipped_recurring)}):")
    for t in plan.skipped_recurring:
        print(f"   • {t.title} ({t.frequency}) — last done {t.last_done}")

if plan.skipped_tasks:
    print(task_table(plan.skipped_tasks,
                     title=f"⚠️  Skipped — didn't fit ({len(plan.skipped_tasks)})"))

if plan.conflicts:
    print("\n🚨 Conflicts:")
    for msg in plan.conflicts:
        icon = "❌" if msg.startswith("CONFLICT") else "⚠️ "
        print(f"   {icon} {msg}")
else:
    print("\n✅ No scheduling conflicts detected.")

print(f"\n💡 Reasoning: {plan.reasoning}")
