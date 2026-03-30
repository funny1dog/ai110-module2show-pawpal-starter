import pytest
from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_scheduler(*tasks, available_minutes=240):
    """Build an Owner + Scheduler pre-loaded with the given tasks."""
    owner = Owner(name="Jordan", available_minutes=available_minutes)
    scheduler = Scheduler(owner=owner)
    for task in tasks:
        scheduler.add_task(task)
    return scheduler


# ---------------------------------------------------------------------------
# Existing tests (kept)
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task(title="Morning Walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(title="Brushing", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 2


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_chronological_order():
    """Tasks added out of order are returned morning → afternoon → evening → any."""
    evening = Task(title="Bedtime Story", duration_minutes=5, priority="low", time_slot="evening")
    any_slot = Task(title="General Task", duration_minutes=5, priority="low", time_slot="any")
    morning = Task(title="Morning Walk", duration_minutes=30, priority="high", time_slot="morning")
    afternoon = Task(title="Play Time", duration_minutes=15, priority="medium", time_slot="afternoon")

    scheduler = make_scheduler(evening, any_slot, morning, afternoon)
    sorted_tasks = scheduler.sort_by_time()

    slots = [t.time_slot for t in sorted_tasks]
    assert slots == ["morning", "afternoon", "evening", "any"]


def test_sort_by_time_does_not_mutate_pool():
    """sort_by_time() must not change the order of self.tasks."""
    t1 = Task(title="Evening Task", duration_minutes=10, priority="low", time_slot="evening")
    t2 = Task(title="Morning Task", duration_minutes=10, priority="high", time_slot="morning")
    scheduler = make_scheduler(t1, t2)

    original_order = [t.title for t in scheduler.tasks]
    scheduler.sort_by_time()
    assert [t.title for t in scheduler.tasks] == original_order


def test_generate_plan_respects_slot_order():
    """Scheduled tasks in the plan appear morning before afternoon before evening."""
    afternoon = Task(title="Grooming", duration_minutes=20, priority="high", time_slot="afternoon")
    morning = Task(title="Walk", duration_minutes=20, priority="high", time_slot="morning")
    evening = Task(title="Meds", duration_minutes=5, priority="high", time_slot="evening")

    scheduler = make_scheduler(afternoon, morning, evening)
    plan = scheduler.generate_plan()
    slots = [t.time_slot for t in plan.scheduled_tasks]
    assert slots == ["morning", "afternoon", "evening"]


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_is_due_today_with_no_last_done():
    """A task never done before is always due."""
    task = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily")
    assert task.is_due_today() is True


def test_daily_task_not_due_same_day():
    """A daily task completed today should not be due again today."""
    task = Task(title="Feeding", duration_minutes=10, priority="high",
                frequency="daily", last_done=date.today())
    assert task.is_due_today() is False


def test_daily_task_due_next_day():
    """A daily task completed yesterday is due today."""
    task = Task(title="Feeding", duration_minutes=10, priority="high",
                frequency="daily", last_done=date.today() - timedelta(days=1))
    assert task.is_due_today() is True


def test_weekly_task_not_due_before_seven_days():
    """A weekly task completed 3 days ago is not yet due."""
    task = Task(title="Brushing", duration_minutes=20, priority="medium",
                frequency="weekly", last_done=date.today() - timedelta(days=3))
    assert task.is_due_today() is False


def test_weekly_task_due_after_seven_days():
    """A weekly task completed exactly 7 days ago is due today."""
    task = Task(title="Brushing", duration_minutes=20, priority="medium",
                frequency="weekly", last_done=date.today() - timedelta(days=7))
    assert task.is_due_today() is True


def test_complete_task_creates_next_occurrence_for_daily():
    """Completing a daily task replaces it with a new instance due tomorrow."""
    task = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily")
    scheduler = make_scheduler(task)

    next_task = scheduler.complete_task("Feeding")

    assert next_task is not None
    assert next_task.title == "Feeding"
    assert next_task.completed is False
    assert next_task.next_due == date.today() + timedelta(days=1)
    assert next_task.is_due_today() is False


def test_complete_task_creates_next_occurrence_for_weekly():
    """Completing a weekly task replaces it with a new instance due in 7 days."""
    task = Task(title="Brushing", duration_minutes=20, priority="medium", frequency="weekly")
    scheduler = make_scheduler(task)

    next_task = scheduler.complete_task("Brushing")

    assert next_task.next_due == date.today() + timedelta(days=7)
    assert next_task.is_due_today() is False


def test_complete_task_pool_size_unchanged():
    """After completing a recurring task the pool still has the same number of tasks."""
    task = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily")
    scheduler = make_scheduler(task)
    assert len(scheduler.tasks) == 1

    scheduler.complete_task("Feeding")
    assert len(scheduler.tasks) == 1


def test_complete_task_unknown_title_raises():
    """complete_task raises ValueError for a title not in the pool."""
    scheduler = make_scheduler()
    with pytest.raises(ValueError, match="No task named"):
        scheduler.complete_task("Nonexistent")


def test_generate_plan_excludes_completed_tasks():
    """Tasks already marked complete do not appear in the scheduled list."""
    done = Task(title="Walk", duration_minutes=30, priority="high")
    done.mark_complete()
    pending = Task(title="Feeding", duration_minutes=10, priority="high")

    scheduler = make_scheduler(done, pending)
    plan = scheduler.generate_plan()

    titles = [t.title for t in plan.scheduled_tasks]
    assert "Walk" not in titles
    assert "Feeding" in titles


def test_generate_plan_excludes_not_due_recurring():
    """A recurring task done today appears in skipped_recurring, not scheduled."""
    task = Task(title="Feeding", duration_minutes=10, priority="high",
                frequency="daily", last_done=date.today())
    scheduler = make_scheduler(task)
    plan = scheduler.generate_plan()

    assert len(plan.scheduled_tasks) == 0
    assert any(t.title == "Feeding" for t in plan.skipped_recurring)


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_no_conflicts_different_slots():
    """Tasks in different slots produce no conflict warnings."""
    morning = Task(title="Walk", duration_minutes=30, priority="high", time_slot="morning")
    afternoon = Task(title="Play", duration_minutes=15, priority="low", time_slot="afternoon")

    scheduler = make_scheduler(morning, afternoon)
    assert scheduler.detect_conflicts(scheduler.tasks) == []


def test_same_pet_same_slot_raises_conflict():
    """Two tasks for the same pet in the same slot produce a CONFLICT warning."""
    pet = Pet(name="Mochi", species="dog")
    t1 = Task(title="Walk", duration_minutes=30, priority="high", time_slot="morning")
    t2 = Task(title="Bath", duration_minutes=15, priority="medium", time_slot="morning")
    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = make_scheduler(t1, t2)
    warnings = scheduler.detect_conflicts(scheduler.tasks)

    assert any("CONFLICT" in w and "Mochi" in w for w in warnings)


def test_cross_pet_same_slot_raises_warning():
    """Tasks for two different pets in the same slot produce a WARNING."""
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    t1 = Task(title="Walk", duration_minutes=30, priority="high", time_slot="morning")
    t2 = Task(title="Feeding", duration_minutes=10, priority="high", time_slot="morning")
    mochi.add_task(t1)
    luna.add_task(t2)

    scheduler = make_scheduler(t1, t2)
    warnings = scheduler.detect_conflicts(scheduler.tasks)

    assert any("WARNING" in w for w in warnings)


def test_any_slot_tasks_never_conflict():
    """Tasks with time_slot='any' are ignored by conflict detection."""
    t1 = Task(title="Task A", duration_minutes=10, priority="low", time_slot="any")
    t2 = Task(title="Task B", duration_minutes=10, priority="low", time_slot="any")

    scheduler = make_scheduler(t1, t2)
    assert scheduler.detect_conflicts(scheduler.tasks) == []


def test_plan_conflicts_surface_in_display():
    """Conflict messages detected during generate_plan appear in display() output."""
    pet = Pet(name="Mochi", species="dog")
    t1 = Task(title="Walk", duration_minutes=10, priority="high", time_slot="morning")
    t2 = Task(title="Bath", duration_minutes=10, priority="high", time_slot="morning")
    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = make_scheduler(t1, t2)
    plan = scheduler.generate_plan()

    assert len(plan.conflicts) > 0
    assert "Conflicts detected" in plan.display()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_pet_with_no_tasks():
    """A pet with no tasks contributes nothing to all_tasks() and the plan."""
    owner = Owner(name="Jordan", available_minutes=60,
                  pets=[Pet(name="Mochi", species="dog")])
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()

    assert plan.scheduled_tasks == []
    assert plan.total_minutes == 0


def test_owner_with_no_available_minutes():
    """When available_minutes is 0, every task is skipped."""
    task = Task(title="Walk", duration_minutes=30, priority="high")
    owner = Owner(name="Jordan", available_minutes=0)
    scheduler = Scheduler(owner=owner)
    scheduler.add_task(task)
    plan = scheduler.generate_plan()

    assert plan.scheduled_tasks == []
    assert len(plan.skipped_tasks) == 1


def test_duplicate_task_title_raises():
    """Adding two tasks with the same title to the same scheduler raises ValueError."""
    t1 = Task(title="Walk", duration_minutes=30, priority="high")
    t2 = Task(title="Walk", duration_minutes=20, priority="medium")
    scheduler = make_scheduler(t1)

    with pytest.raises(ValueError, match="already exists"):
        scheduler.add_task(t2)


def test_filter_tasks_by_pet():
    """filter_tasks returns only tasks belonging to the specified pet."""
    mochi_task = Task(title="Walk", duration_minutes=30, priority="high")
    luna_task = Task(title="Feeding", duration_minutes=10, priority="high")
    Pet(name="Mochi", species="dog").add_task(mochi_task)
    Pet(name="Luna", species="cat").add_task(luna_task)

    scheduler = make_scheduler(mochi_task, luna_task)
    result = scheduler.filter_tasks(pet_name="Mochi")

    assert all(t.pet_name == "Mochi" for t in result)
    assert len(result) == 1


def test_filter_tasks_by_completion():
    """filter_tasks(completed=False) excludes tasks already marked done."""
    done = Task(title="Walk", duration_minutes=30, priority="high")
    done.mark_complete()
    pending = Task(title="Feeding", duration_minutes=10, priority="high")

    scheduler = make_scheduler(done, pending)
    result = scheduler.filter_tasks(completed=False)

    assert all(not t.completed for t in result)
    assert len(result) == 1


def test_special_needs_boost_schedules_before_lower_priority():
    """A medium-priority task matching special_needs is scheduled before other mediums."""
    pet = Pet(name="Mochi", species="dog", special_needs=["joint supplement"])
    supplement = Task(title="Joint Supplement", duration_minutes=5,
                      priority="medium", category="health", time_slot="morning")
    grooming = Task(title="Brushing", duration_minutes=20,
                    priority="medium", category="grooming", time_slot="morning")
    pet.add_task(supplement)
    pet.add_task(grooming)

    owner = Owner(name="Jordan", available_minutes=60, pets=[pet])
    scheduler = Scheduler(owner=owner)
    for task in owner.all_tasks():
        scheduler.add_task(task)

    plan = scheduler.generate_plan()
    titles = [t.title for t in plan.scheduled_tasks]
    assert titles.index("Joint Supplement") < titles.index("Brushing")


# ---------------------------------------------------------------------------
# Effort scoring
# ---------------------------------------------------------------------------

def test_effort_score_empty_plan_is_light():
    """An empty plan always returns score 0 and label 'Light'."""
    owner = Owner(name="Jordan", available_minutes=60)
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()
    result = plan.effort_score()

    assert result["score"] == 0
    assert result["label"] == "Light"


def test_effort_score_zero_available_minutes_is_light():
    """A plan with available_minutes=0 returns score 0 without dividing by zero."""
    task = Task(title="Walk", duration_minutes=30, priority="high")
    owner = Owner(name="Jordan", available_minutes=0)
    scheduler = Scheduler(owner=owner)
    scheduler.add_task(task)
    plan = scheduler.generate_plan()
    result = plan.effort_score()

    assert result["score"] == 0
    assert result["label"] == "Light"


def test_effort_score_has_three_breakdown_keys():
    """effort_score() always returns all three breakdown components."""
    task = Task(title="Walk", duration_minutes=20, priority="high", category="exercise")
    scheduler = make_scheduler(task, available_minutes=60)
    plan = scheduler.generate_plan()
    result = plan.effort_score()

    assert set(result["breakdown"].keys()) == {"time_utilization", "priority_weight", "task_variety"}


def test_effort_score_increases_with_more_high_priority_tasks():
    """A plan with more high-priority tasks scores higher than one with low-priority tasks."""
    high1 = Task(title="Meds", duration_minutes=10, priority="high", category="health")
    high2 = Task(title="Walk", duration_minutes=10, priority="high", category="exercise")
    low1 = Task(title="Play", duration_minutes=10, priority="low", category="enrichment")
    low2 = Task(title="Nap", duration_minutes=10, priority="low", category="general")

    sched_high = make_scheduler(high1, high2, available_minutes=60)
    sched_low = make_scheduler(low1, low2, available_minutes=60)

    score_high = sched_high.generate_plan().effort_score()["score"]
    score_low = sched_low.generate_plan().effort_score()["score"]

    assert score_high > score_low


def test_effort_score_increases_with_task_variety():
    """A plan covering more categories scores higher than one repeating the same category."""
    varied = [
        Task(title="Meds", duration_minutes=10, priority="medium", category="health"),
        Task(title="Feeding", duration_minutes=10, priority="medium", category="nutrition"),
        Task(title="Walk", duration_minutes=10, priority="medium", category="exercise"),
        Task(title="Grooming", duration_minutes=10, priority="medium", category="grooming"),
    ]
    repetitive = [
        Task(title="Walk A", duration_minutes=10, priority="medium", category="exercise"),
        Task(title="Walk B", duration_minutes=10, priority="medium", category="exercise"),
        Task(title="Walk C", duration_minutes=10, priority="medium", category="exercise"),
        Task(title="Walk D", duration_minutes=10, priority="medium", category="exercise"),
    ]

    score_varied = make_scheduler(*varied, available_minutes=120).generate_plan().effort_score()["score"]
    score_repetitive = make_scheduler(*repetitive, available_minutes=120).generate_plan().effort_score()["score"]

    assert score_varied > score_repetitive


def test_effort_score_label_reflects_score():
    """The label returned matches the score's band."""
    task = Task(title="Walk", duration_minutes=5, priority="low", category="exercise")
    scheduler = make_scheduler(task, available_minutes=120)
    plan = scheduler.generate_plan()
    result = plan.effort_score()

    score = result["score"]
    label = result["label"]
    if score <= 25:
        assert label == "Light"
    elif score <= 50:
        assert label == "Moderate"
    elif score <= 75:
        assert label == "Demanding"
    else:
        assert label == "Heavy"
