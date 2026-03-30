from datetime import date, timedelta

VALID_PRIORITIES = {"low", "medium", "high"}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
CATEGORY_ORDER = {"health": 0, "nutrition": 1, "exercise": 2, "grooming": 3, "enrichment": 4, "general": 5}
VALID_TIME_SLOTS = {"morning", "afternoon", "evening", "any"}
SLOT_ORDER = {"morning": 0, "afternoon": 1, "evening": 2, "any": 3}
SLOT_MAX_MINUTES = 180  # flag a slot as overbooked beyond 3 hours
FREQUENCY_DAYS = {"daily": 1, "weekly": 7}  # used by timedelta to compute next due date


class Pet:
    def __init__(self, name: str, species: str, special_needs: list[str] = None):
        self.name = name
        self.species = species
        self.special_needs = special_needs or []
        self.tasks: list["Task"] = []

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet, raising ValueError if the title already exists."""
        if any(t.title == task.title for t in self.tasks):
            raise ValueError(f"A task named '{task.title}' already exists for {self.name}")
        task.pet_name = self.name  # tag the task with its owning pet
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove the task with the given title from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.title != title]


class Owner:
    def __init__(self, name: str, available_minutes: int, pets: list[Pet] = None, preferences: list[str] = None):
        if available_minutes < 0:
            raise ValueError("available_minutes cannot be negative")
        self.name = name
        self.available_minutes = available_minutes
        self.pets = pets or []
        self.preferences = preferences or []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def all_tasks(self) -> list["Task"]:
        """Return a flat list of all tasks across every pet this owner has."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Task:
    def __init__(
        self,
        title: str,
        duration_minutes: int,
        priority: str,
        category: str = "general",
        frequency: str = "daily",
        time_slot: str = "any",
        last_done: date | None = None,
    ):
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}, got '{priority}'")
        if time_slot not in VALID_TIME_SLOTS:
            raise ValueError(f"time_slot must be one of {VALID_TIME_SLOTS}, got '{time_slot}'")
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.frequency = frequency
        self.time_slot = time_slot
        self.last_done = last_done
        self.next_due: date | None = None  # set explicitly by next_occurrence() via timedelta
        self.pet_name = ""  # set automatically by Pet.add_task()
        self.completed = False

    def is_due_today(self) -> bool:
        """Return True if this task should appear in today's plan.

        If next_due was set by next_occurrence(), compare directly against today.
        Otherwise fall back to last_done + frequency calculation.
        """
        if self.next_due is not None:
            return date.today() >= self.next_due
        if self.last_done is None:
            return True
        delta = (date.today() - self.last_done).days
        if self.frequency == "daily":
            return delta >= 1
        if self.frequency == "weekly":
            return delta >= 7
        return True

    def mark_complete(self) -> None:
        """Mark this task as completed and record today as last_done."""
        self.completed = True
        self.last_done = date.today()

    def next_occurrence(self) -> "Task":
        """Return a fresh, incomplete copy of this task scheduled for its next due date.

        Uses FREQUENCY_DAYS and timedelta to compute next_due exactly:
          - daily  → next_due = today + 1 day
          - weekly → next_due = today + 7 days

        The new task inherits all attributes (title, duration, priority, category,
        time_slot, pet_name) but starts with completed=False and last_done=today.
        is_due_today() on the returned task will return False until next_due arrives.

        Raises ValueError if frequency is not 'daily' or 'weekly'.
        """
        if self.frequency not in FREQUENCY_DAYS:
            raise ValueError(f"next_occurrence() is only valid for daily/weekly tasks, not '{self.frequency}'")
        task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            time_slot=self.time_slot,
            last_done=date.today(),
        )
        task.next_due = date.today() + timedelta(days=FREQUENCY_DAYS[self.frequency])
        task.pet_name = self.pet_name
        return task

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is high."""
        return self.priority == "high"

    def to_dict(self) -> dict:
        """Serialize this task to a dictionary for display or storage."""
        return {
            "title": self.title,
            "pet": self.pet_name,
            "time_slot": self.time_slot,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "category": self.category,
            "frequency": self.frequency,
            "completed": self.completed,
            "last_done": str(self.last_done) if self.last_done else None,
        }


class DailyPlan:
    def __init__(
        self,
        owner: Owner,
        scheduled_tasks: list[Task],
        skipped_tasks: list[Task],
        skipped_recurring: list[Task],
        conflicts: list[str],
        reasoning: str,
    ):
        self.owner = owner
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.skipped_recurring = skipped_recurring
        self.conflicts = conflicts
        self.total_minutes = sum(t.duration_minutes for t in scheduled_tasks)
        self.reasoning = reasoning

    def effort_score(self) -> dict:
        """Return a composite effort score (0–100) rating how demanding this plan is.

        The score is built from three independent components:

        1. Time utilization (0–40 pts)
           total_minutes / available_minutes × 40.
           A plan that uses all available time scores the full 40.

        2. Priority weight (0–40 pts)
           Each scheduled task contributes points based on its priority:
             high → 3 pts,  medium → 1 pt,  low → 0 pts.
           The raw sum is scaled (× 4) and capped at 40 so a single
           high-priority task doesn't dominate the score.

        3. Task variety (0–20 pts)
           5 pts per unique category present in the scheduled list, capped at 20.
           A plan covering health, nutrition, exercise, and enrichment scores
           higher than one that repeats the same category four times.

        Score labels:
            0–25  → "Light"
            26–50 → "Moderate"
            51–75 → "Demanding"
            76–100 → "Heavy"

        Returns a dict with keys: score, label, breakdown.
        Never raises — returns score 0 / label "Light" for an empty plan.
        """
        if not self.scheduled_tasks or self.owner.available_minutes == 0:
            return {"score": 0, "label": "Light",
                    "breakdown": {"time_utilization": 0, "priority_weight": 0, "task_variety": 0}}

        # Component 1: time utilization
        time_score = round((self.total_minutes / self.owner.available_minutes) * 40)

        # Component 2: priority weight
        priority_points = {"high": 3, "medium": 1, "low": 0}
        raw_priority = sum(priority_points[t.priority] for t in self.scheduled_tasks)
        priority_score = min(40, raw_priority * 4)

        # Component 3: task variety
        unique_categories = len({t.category for t in self.scheduled_tasks})
        variety_score = min(20, unique_categories * 5)

        total = time_score + priority_score + variety_score

        if total <= 25:
            label = "Light"
        elif total <= 50:
            label = "Moderate"
        elif total <= 75:
            label = "Demanding"
        else:
            label = "Heavy"

        return {
            "score": total,
            "label": label,
            "breakdown": {
                "time_utilization": time_score,
                "priority_weight": priority_score,
                "task_variety": variety_score,
            },
        }

    def display(self) -> str:
        """Return a formatted string summary of the daily plan grouped by time slot."""
        lines = [f"=== {self.owner.name}'s Daily Plan ==="]

        # Group scheduled tasks by time slot
        slots = ["morning", "afternoon", "evening", "any"]
        for slot in slots:
            slot_tasks = [t for t in self.scheduled_tasks if t.time_slot == slot]
            if slot_tasks:
                label = slot.capitalize() if slot != "any" else "Unslotted"
                lines.append(f"\n[{label}]")
                for task in slot_tasks:
                    pet_label = f" ({task.pet_name})" if task.pet_name else ""
                    lines.append(f"  [{task.priority.upper()}] {task.title}{pet_label} — {task.duration_minutes} min")

        if not self.scheduled_tasks:
            lines.append("\nNo tasks scheduled.")

        lines.append(f"\nTotal time: {self.total_minutes} min / {self.owner.available_minutes} min available")

        if self.skipped_recurring:
            lines.append("\nSkipped (not due today):")
            for task in self.skipped_recurring:
                lines.append(f"  {task.title} — last done {task.last_done} ({task.frequency})")

        if self.skipped_tasks:
            lines.append("\nSkipped (didn't fit):")
            for task in self.skipped_tasks:
                lines.append(f"  {task.title} ({task.duration_minutes} min)")

        if self.conflicts:
            lines.append("\n⚠ Conflicts detected:")
            for conflict in self.conflicts:
                lines.append(f"  - {conflict}")

        lines.append(f"\nReasoning: {self.reasoning}")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduling pool, raising ValueError if the title already exists."""
        if any(t.title == task.title for t in self.tasks):
            raise ValueError(f"A task named '{task.title}' already exists")
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove the task with the given title from the scheduling pool."""
        self.tasks = [t for t in self.tasks if t.title != title]

    def sort_by_time(self) -> list[Task]:
        """Return all tasks in the pool sorted by time slot order.

        Order: morning → afternoon → evening → any (unslotted tasks last).
        Tasks within the same slot keep their relative insertion order.
        Does not modify self.tasks — returns a new sorted list.
        Useful for previewing task order without running a full plan.
        """
        return sorted(self.tasks, key=lambda t: SLOT_ORDER[t.time_slot])

    def complete_task(self, title: str) -> "Task | None":
        """Mark a task complete and, for recurring tasks, swap in its next occurrence.

        Steps:
          1. Locate the task by title (raises ValueError if not found).
          2. Call task.mark_complete(), which sets completed=True and last_done=today.
          3. If frequency is 'daily' or 'weekly':
               - Call task.next_occurrence() to get a fresh copy with next_due set via timedelta.
               - Remove the completed task from the pool.
               - Append the next occurrence so it reappears on its next due date.
               - Return the new Task.
          4. For one-off tasks (any other frequency): return None.

        The pool size stays constant for recurring tasks — the old entry is replaced,
        not duplicated.
        """
        task = next((t for t in self.tasks if t.title == title), None)
        if task is None:
            raise ValueError(f"No task named '{title}' in scheduler")
        task.mark_complete()
        if task.frequency in ("daily", "weekly"):
            next_task = task.next_occurrence()
            self.remove_task(title)
            self.tasks.append(next_task)
            return next_task
        return None

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Scan a task list for time-slot overlaps and return human-readable warning strings.

        Two conflict levels are detected:
          CONFLICT — same pet has more than one task in the same named slot
                     (e.g. Mochi has both 'Morning Walk' and 'Bath Time' in morning).
          WARNING  — tasks for different pets share a slot, meaning the owner
                     would need to handle both simultaneously.

        Algorithm:
          1. Group tasks by time_slot, skipping 'any' (no fixed time).
          2. For each slot with 2+ tasks, sub-group by pet_name.
          3. Emit a CONFLICT message for any pet with 2+ tasks in that slot.
          4. Emit a WARNING message if 2+ distinct pets appear in that slot.

        Args:
            tasks: list of Task objects to inspect (typically plan.scheduled_tasks).

        Returns:
            A list of warning strings; empty if no conflicts found.
            Never raises an exception.
        """
        warnings = []
        # Group tasks by slot, ignoring 'any'
        slot_map: dict[str, list[Task]] = {}
        for task in tasks:
            if task.time_slot == "any":
                continue
            slot_map.setdefault(task.time_slot, []).append(task)

        for slot, slot_tasks in slot_map.items():
            if len(slot_tasks) < 2:
                continue
            # Group within this slot by pet
            pet_map: dict[str, list[Task]] = {}
            for task in slot_tasks:
                pet_map.setdefault(task.pet_name or "unknown", []).append(task)

            # Same-pet conflict: one pet has multiple tasks in the same slot
            for pet, pet_tasks in pet_map.items():
                if len(pet_tasks) > 1:
                    titles = ", ".join(t.title for t in pet_tasks)
                    warnings.append(
                        f"CONFLICT [{slot}] {pet} has {len(pet_tasks)} tasks at the same time: {titles}"
                    )

            # Cross-pet conflict: owner must handle tasks for different pets simultaneously
            pets_in_slot = [p for p in pet_map if p]
            if len(pets_in_slot) > 1:
                warnings.append(
                    f"WARNING  [{slot}] tasks for {' and '.join(pets_in_slot)} overlap "
                    f"— owner cannot do both at the same time"
                )

        return warnings

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list[Task]:
        """Return a filtered view of the task pool. Does not modify self.tasks.

        Args:
            pet_name:  If provided, keep only tasks whose pet_name matches exactly.
            completed: If True, keep only completed tasks.
                       If False, keep only incomplete tasks.
                       If None (default), completion status is not filtered.

        Both filters are applied together when both are provided.
        Returns an empty list if no tasks match — never raises.
        """
        result = self.tasks
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def generate_plan(self) -> DailyPlan:
        """Build today's DailyPlan from the current task pool in four stages.

        Stage 1 — Recurring filter:
            Exclude tasks that are already completed or not yet due (is_due_today()
            returns False). These go into skipped_recurring for display only.

        Stage 2 — Sorting:
            Due tasks are sorted by a five-key tuple:
              (slot_order, frequency_order, effective_priority, category_order, duration)
            - slot_order:       morning=0, afternoon=1, evening=2, any=3
            - frequency_order:  daily=0, other=1  (daily tasks run before weekly)
            - effective_priority: tasks whose title matches an owner pet's special_needs
                                  are promoted to 'high' regardless of their set priority
            - category_order:   health → nutrition → exercise → grooming → enrichment
            - duration:         shorter tasks break ties within the same category

        Stage 3 — Greedy scheduling:
            Iterate sorted tasks; add each to the schedule if it fits within remaining
            available_minutes. Tasks that don't fit go into skipped_tasks.

        Stage 4 — Conflict detection:
            Call detect_conflicts(scheduled) to flag same-pet and cross-pet slot overlaps
            in the final scheduled list.

        Returns:
            A DailyPlan containing scheduled tasks, both skip lists, conflict warnings,
            and a human-readable reasoning string.
        """
        special_needs = {need.lower() for pet in self.owner.pets for need in pet.special_needs}

        def effective_priority(task: Task) -> str:
            if task.title.lower() in special_needs:
                return "high"
            return task.priority

        # Recurring task filter: skip tasks already done within their frequency window
        due_tasks = [t for t in self.tasks if not t.completed and t.is_due_today()]
        skipped_recurring = [t for t in self.tasks if not t.completed and not t.is_due_today()]

        # Sort: time slot → daily-first → boosted priority → category → duration
        sorted_tasks = sorted(
            due_tasks,
            key=lambda t: (
                SLOT_ORDER[t.time_slot],
                0 if t.frequency == "daily" else 1,
                PRIORITY_ORDER[effective_priority(t)],
                CATEGORY_ORDER.get(t.category, len(CATEGORY_ORDER)),
                t.duration_minutes,
            )
        )

        # Greedy scheduling
        scheduled = []
        skipped = []
        remaining = self.owner.available_minutes
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                scheduled.append(task)
                remaining -= task.duration_minutes
            else:
                skipped.append(task)

        # Conflict detection: same-pet and cross-pet slot overlaps
        conflicts = self.detect_conflicts(scheduled)

        boosted = [t.title for t in self.tasks if t.title.lower() in special_needs and t.priority != "high"]
        reasoning = (
            f"Recurring tasks not yet due were excluded ({len(skipped_recurring)} skipped). "
            f"Remaining tasks sorted by time slot, then daily-first frequency, then priority"
            + (f" (special-needs boost applied to: {boosted})" if boosted else "")
            + f", then category, then duration. "
            f"{len(scheduled)} scheduled, {len(skipped)} skipped (time), {len(conflicts)} conflict(s) flagged."
        )
        return DailyPlan(
            owner=self.owner,
            scheduled_tasks=scheduled,
            skipped_tasks=skipped,
            skipped_recurring=skipped_recurring,
            conflicts=conflicts,
            reasoning=reasoning,
        )
