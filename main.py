from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup pets ---
mochi = Pet(name="Mochi", species="dog", special_needs=["joint supplement"])
luna = Pet(name="Luna", species="cat")

# --- Setup owner ---
jordan = Owner(name="Jordan", available_minutes=90, pets=[mochi, luna])

# --- Create tasks ---
morning_walk = Task(title="Morning Walk", duration_minutes=30, priority="high", category="exercise")
feeding = Task(title="Feeding", duration_minutes=10, priority="high", category="nutrition", frequency="daily")
medication = Task(title="Joint Supplement", duration_minutes=5, priority="high", category="health")
grooming = Task(title="Brushing", duration_minutes=20, priority="medium", category="grooming")
enrichment = Task(title="Toy Enrichment", duration_minutes=15, priority="low", category="enrichment")

# --- Add tasks to scheduler ---
scheduler = Scheduler(owner=jordan)
for task in [morning_walk, feeding, medication, grooming, enrichment]:
    scheduler.add_task(task)

# --- Generate and print plan ---
plan = scheduler.generate_plan()
print(plan.display())
