import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=1, max_value=1440, value=120)

# Initialize the Owner in session_state once — reuses the same object on every rerun
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)

st.divider()

st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(pet)
    st.success(f"Added pet: {pet_name} ({species})")

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species} for p in st.session_state.owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
st.caption("Select a pet and add a care task for them.")

if st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_pet = st.selectbox("Assign to pet", pet_names)
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        try:
            task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
            pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
            pet.add_task(task)
            st.success(f"Added task '{task_title}' to {selected_pet}")
        except ValueError as e:
            st.error(str(e))
else:
    st.info("Add a pet first before adding tasks.")

owner_tasks = st.session_state.owner.all_tasks()
if owner_tasks:
    st.write("Current tasks:")
    st.table([t.to_dict() for t in owner_tasks])
else:
    st.info("No tasks yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    owner = st.session_state.owner
    scheduler = Scheduler(owner=owner)
    for task in owner.all_tasks():
        scheduler.add_task(task)
    plan = scheduler.generate_plan()
    st.markdown(f"### {owner.name}'s Daily Plan")
    if plan.scheduled_tasks:
        st.write("**Scheduled tasks:**")
        st.table([t.to_dict() for t in plan.scheduled_tasks])
    else:
        st.info("No tasks could be scheduled.")
    if plan.skipped_tasks:
        st.write("**Skipped (didn't fit):**")
        st.table([t.to_dict() for t in plan.skipped_tasks])
    st.write(f"**Total time:** {plan.total_minutes} / {owner.available_minutes} min")
    st.caption(f"Reasoning: {plan.reasoning}")
