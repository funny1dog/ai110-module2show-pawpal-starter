class Pet:
    def __init__(self, name: str, species: str, special_needs: list[str] = None):
        self.name = name
        self.species = species
        self.special_needs = special_needs or []


class Owner:
    def __init__(self, name: str, available_minutes: int, pet: Pet, preferences: list[str] = None):
        self.name = name
        self.available_minutes = available_minutes
        self.pet = pet
        self.preferences = preferences or []


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str, category: str = "general"):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority  # "low", "medium", "high"
        self.category = category

    def is_high_priority(self) -> bool:
        ...

    def to_dict(self) -> dict:
        ...


class DailyPlan:
    def __init__(self, scheduled_tasks: list[Task], skipped_tasks: list[Task], reasoning: str):
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.total_minutes = None  # TODO: compute from scheduled_tasks
        self.reasoning = reasoning

    def display(self) -> str:
        ...


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def generate_plan(self) -> DailyPlan:
        ...
