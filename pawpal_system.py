VALID_PRIORITIES = {"low", "medium", "high"}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


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
    def __init__(self, title: str, duration_minutes: int, priority: str, category: str = "general", frequency: str = "daily"):
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}, got '{priority}'")
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.frequency = frequency
        self.completed = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is high."""
        return self.priority == "high"

    def to_dict(self) -> dict:
        """Serialize this task to a dictionary for display or storage."""
        return {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "category": self.category,
            "frequency": self.frequency,
            "completed": self.completed,
        }


class DailyPlan:
    def __init__(self, owner: Owner, scheduled_tasks: list[Task], skipped_tasks: list[Task], reasoning: str):
        self.owner = owner
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.total_minutes = sum(t.duration_minutes for t in scheduled_tasks)
        self.reasoning = reasoning

    def display(self) -> str:
        """Return a formatted string summary of the daily plan for terminal output."""
        lines = [f"=== {self.owner.name}'s Daily Plan ==="]
        if self.scheduled_tasks:
            lines.append("\nScheduled Tasks:")
            for task in self.scheduled_tasks:
                lines.append(f"  [{task.priority.upper()}] {task.title} — {task.duration_minutes} min")
        else:
            lines.append("\nNo tasks scheduled.")
        lines.append(f"\nTotal time: {self.total_minutes} min / {self.owner.available_minutes} min available")
        if self.skipped_tasks:
            lines.append("\nSkipped Tasks:")
            for task in self.skipped_tasks:
                lines.append(f"  {task.title} ({task.duration_minutes} min) — didn't fit")
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

    def generate_plan(self) -> DailyPlan:
        """Sort tasks by priority and duration, greedily schedule what fits, and return a DailyPlan."""
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (PRIORITY_ORDER[t.priority], t.duration_minutes)
        )
        scheduled = []
        skipped = []
        remaining = self.owner.available_minutes
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                scheduled.append(task)
                remaining -= task.duration_minutes
            else:
                skipped.append(task)
        reasoning = (
            f"Tasks were sorted by priority (high → medium → low) then by duration. "
            f"{len(scheduled)} task(s) fit within {self.owner.available_minutes} minutes. "
            f"{len(skipped)} task(s) were skipped due to time constraints."
        )
        return DailyPlan(
            owner=self.owner,
            scheduled_tasks=scheduled,
            skipped_tasks=skipped,
            reasoning=reasoning,
        )
