# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

The scheduling logic in `pawpal_system.py` goes beyond a simple priority sort. Here is what it does and why.

**Time-slot ordering**
Each `Task` has a `time_slot` (`morning`, `afternoon`, `evening`, or `any`). The scheduler always places morning tasks before afternoon tasks before evening tasks, giving the plan a natural daily flow regardless of the order tasks were added.

**Recurring task filtering**
Tasks carry a `frequency` (`daily` or `weekly`) and a `last_done` date. Before scheduling, the `Scheduler` calls `Task.is_due_today()` on every task and silently excludes anything that has already been done within its recurrence window. Excluded tasks are listed separately in the plan as "Skipped (not due today)" so the owner can see them without acting on them.

**Automatic next occurrence**
When `Scheduler.complete_task(title)` is called, it marks the task done and — for daily/weekly tasks — immediately creates a replacement using `Task.next_occurrence()`. The replacement's `next_due` date is computed with Python's `timedelta` (`today + 1 day` for daily, `today + 7 days` for weekly), so the task reappears in the plan exactly when it should.

**Special-needs priority boost**
If a `Pet` lists a condition in `special_needs` (e.g. `"joint supplement"`), any task whose title matches that condition is automatically treated as high priority during scheduling, even if it was added with a lower priority. This prevents health-critical tasks from being bumped by convenience tasks.

**Conflict detection**
After greedy scheduling, `Scheduler.detect_conflicts()` scans the final task list and emits two levels of warning — neither stops the program:

- `CONFLICT` — the same pet has more than one task assigned to the same named slot.
- `WARNING` — tasks for different pets share a slot, meaning the owner would need to be in two places at once.

Warnings appear at the bottom of the plan output under "Conflicts detected."

**Filtering and sorting utilities**
Two helper methods make it easy to inspect the task pool without generating a full plan:

- `Scheduler.sort_by_time()` — returns tasks ordered by slot (morning → afternoon → evening → unslotted).
- `Scheduler.filter_tasks(pet_name, completed)` — returns a filtered subset by pet and/or completion status.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
