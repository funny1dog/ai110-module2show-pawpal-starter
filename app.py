import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, save_data, load_data

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
PRIORITY_EMOJI = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
SLOT_EMOJI = {"morning": "🌅 morning", "afternoon": "☀️ afternoon", "evening": "🌙 evening", "any": "🔄 any"}

def task_rows(tasks):
    """Return display-ready dicts with priority, slot, and completion emoji for st.dataframe."""
    rows = []
    for t in tasks:
        d = t.to_dict()
        d["priority"] = PRIORITY_EMOJI.get(t.priority, t.priority)
        d["time_slot"] = SLOT_EMOJI.get(t.time_slot, t.time_slot)
        d["completed"] = "✅ Done" if t.completed else "⬜ Pending"
        rows.append(d)
    return rows

st.title("🐾 PawPal+")
st.caption("A smart pet care planner that sorts, filters, and checks for scheduling conflicts.")

st.divider()

# ---------------------------------------------------------------------------
# Owner setup
# ---------------------------------------------------------------------------
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=0, max_value=1440, value=120)

if "owner" not in st.session_state:
    loaded = load_data()
    st.session_state.owner = loaded if loaded else Owner(name=owner_name, available_minutes=available_minutes)

st.divider()

# ---------------------------------------------------------------------------
# Add a Pet
# ---------------------------------------------------------------------------
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(pet)
    save_data(st.session_state.owner)
    st.success(f"Added {pet_name} ({species}) to your household.")

if st.session_state.owner.pets:
    st.dataframe(
        [{"name": p.name, "species": p.species, "tasks": len(p.tasks)}
         for p in st.session_state.owner.pets],
        use_container_width=True,
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Add a Task
# ---------------------------------------------------------------------------
st.subheader("Add a Task")

if st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("Assign to pet", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        time_slot = st.selectbox("Time slot", ["morning", "afternoon", "evening", "any"])
        frequency = st.selectbox("Frequency", ["daily", "weekly"])

    if st.button("Add task"):
        try:
            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                time_slot=time_slot,
                frequency=frequency,
            )
            pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
            pet.add_task(task)
            save_data(st.session_state.owner)
            st.success(f"Added '{task_title}' to {selected_pet}.")
        except ValueError as e:
            st.error(str(e))
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# ---------------------------------------------------------------------------
# Task inspector — sort_by_time() + filter_tasks()
# ---------------------------------------------------------------------------
st.subheader("Task Inspector")

all_tasks = st.session_state.owner.all_tasks()

if all_tasks:
    scheduler = Scheduler(owner=st.session_state.owner)
    for task in all_tasks:
        scheduler.add_task(task)

    col1, col2 = st.columns(2)
    with col1:
        filter_pet = st.selectbox(
            "Filter by pet",
            ["All"] + [p.name for p in st.session_state.owner.pets],
        )
    with col2:
        filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    pet_arg = None if filter_pet == "All" else filter_pet
    completed_arg = None if filter_status == "All" else (filter_status == "Completed")
    filtered = scheduler.filter_tasks(pet_name=pet_arg, completed=completed_arg)

    # Show filtered tasks sorted by time slot using sort_by_time logic
    sorted_filtered = sorted(filtered, key=lambda t: ["morning", "afternoon", "evening", "any"].index(t.time_slot))

    if sorted_filtered:
        st.caption(f"{len(sorted_filtered)} task(s) — sorted by time slot")
        st.dataframe(task_rows(sorted_filtered), use_container_width=True)
    else:
        st.info("No tasks match the selected filters.")

    # Conflict preview on current task pool
    pool_conflicts = scheduler.detect_conflicts(all_tasks)
    if pool_conflicts:
        st.markdown("**Scheduling conflicts in current tasks:**")
        for msg in pool_conflicts:
            if msg.startswith("CONFLICT"):
                st.warning(msg)
            else:
                st.info(msg)
else:
    st.info("No tasks added yet.")

st.divider()

# ---------------------------------------------------------------------------
# Complete Tasks
# ---------------------------------------------------------------------------
st.subheader("Complete Tasks")

all_tasks_for_complete = st.session_state.owner.all_tasks()
if all_tasks_for_complete:
    st.caption("Check a task to mark it complete. Recurring tasks will auto-schedule their next occurrence.")
    for task in all_tasks_for_complete:
        PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        recurring_badge = " 🔁" if task.frequency in ("daily", "weekly") else ""
        label = (
            f"{PRIORITY_ICON.get(task.priority, '')} {task.title} "
            f"({task.pet_name}) — {task.duration_minutes} min{recurring_badge}"
        )
        checked = st.checkbox(label, value=task.completed, key=f"complete_{task.title}_{task.pet_name}")
        if checked and not task.completed:
            # Find the pet that owns this task
            pet = next(p for p in st.session_state.owner.pets if p.name == task.pet_name)
            if task.frequency in ("daily", "weekly"):
                # Replace with next occurrence so the task reappears when due
                next_task = task.next_occurrence()
                pet.remove_task(task.title)
                pet.add_task(next_task)
            else:
                task.mark_complete()
            save_data(st.session_state.owner)
            st.rerun()
else:
    st.info("No tasks to complete yet.")

st.divider()

# ---------------------------------------------------------------------------
# Generate Schedule
# ---------------------------------------------------------------------------
st.subheader("Generate Schedule")

if st.button("Generate schedule", type="primary"):
    owner = st.session_state.owner
    if not owner.all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner)
        for task in owner.all_tasks():
            scheduler.add_task(task)
        plan = scheduler.generate_plan()

        st.markdown(f"### {owner.name}'s Daily Plan")
        st.caption(f"Budget: {plan.total_minutes} / {owner.available_minutes} min used")

        # Effort score
        effort = plan.effort_score()
        label_color = {"Light": "🟢", "Moderate": "🟡", "Demanding": "🟠", "Heavy": "🔴"}
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Day Load", f"{label_color[effort['label']]} {effort['label']}")
        col2.metric("Effort Score", f"{effort['score']} / 100")
        col3.metric("Time Utilization", f"{effort['breakdown']['time_utilization']} pts")
        col4.metric("Priority Weight", f"{effort['breakdown']['priority_weight']} pts")
        st.progress(effort["score"] / 100)

        # Scheduled tasks grouped by time slot
        slots = ["morning", "afternoon", "evening", "any"]
        slot_labels = {"morning": "Morning", "afternoon": "Afternoon",
                       "evening": "Evening", "any": "Unslotted"}
        scheduled_any = False
        for slot in slots:
            slot_tasks = [t for t in plan.scheduled_tasks if t.time_slot == slot]
            if slot_tasks:
                scheduled_any = True
                st.markdown(f"**{slot_labels[slot]}**")
                st.dataframe(task_rows(slot_tasks), use_container_width=True)

        if not scheduled_any:
            st.info("No tasks could be scheduled within the available time.")

        # Skipped — recurring not due
        if plan.skipped_recurring:
            with st.expander(f"Skipped — not due today ({len(plan.skipped_recurring)})"):
                for t in plan.skipped_recurring:
                    st.caption(f"{t.title} ({t.frequency}) — last done {t.last_done}")

        # Skipped — didn't fit
        if plan.skipped_tasks:
            with st.expander(f"Skipped — didn't fit ({len(plan.skipped_tasks)})"):
                st.dataframe(task_rows(plan.skipped_tasks), use_container_width=True)

        # Conflict warnings
        if plan.conflicts:
            st.markdown("**Conflicts detected:**")
            for msg in plan.conflicts:
                if msg.startswith("CONFLICT"):
                    st.warning(msg)
                else:
                    st.info(msg)
        else:
            st.success("No scheduling conflicts detected.")

        # Reasoning
        with st.expander("How this plan was built"):
            st.caption(plan.reasoning)
