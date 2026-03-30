import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling — powered by Python OOP")

# --- Session state ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# --- Owner Info ---
st.subheader("👤 Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=owner.name or "Jordan")
with col2:
    owner_email = st.text_input("Email", value=owner.email or "jordan@email.com")
if st.button("Save Owner"):
    owner.name = owner_name
    owner.email = owner_email
    st.success(f"✅ Owner saved: {owner.name}")

st.divider()

# --- Add a Pet ---
st.subheader("🐶 Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    if pet_name.lower() in [p.name.lower() for p in owner.pets]:
        st.warning(f"⚠️ {pet_name} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, age=age))
        st.success(f"✅ {pet_name} the {species} added!")

if owner.pets:
    st.info("🐾 Pets: " + ", ".join(p.name for p in owner.pets))

st.divider()

# --- Schedule a Task ---
st.subheader("📋 Schedule a Task")
if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("Pet", [p.name for p in owner.pets])
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    col3, col4 = st.columns(2)
    with col3:
        task_desc = st.text_input("Task description", value="Morning walk")
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        pet = next(p for p in owner.pets if p.name == selected_pet)
        pet.add_task(Task(
            description=task_desc,
            time=task_time,
            frequency=frequency,
            due_date=date.today()
        ))
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for c in conflicts:
                st.warning(f"⚠️ Conflict: {c}")
        else:
            st.success(f"✅ '{task_desc}' added for {selected_pet} at {task_time}.")

st.divider()

# --- Today's Schedule ---
st.subheader("📅 Today's Schedule")
if st.button("Generate Schedule"):
    sorted_tasks = scheduler.sort_by_time()
    if not sorted_tasks:
        st.info("No tasks scheduled yet.")
    else:
        for pet in owner.pets:
            pet_tasks = [t for t in sorted_tasks if t in pet.get_tasks()]
            if pet_tasks:
                st.markdown(f"**{pet.name}** ({pet.species})")
                st.table([{
                    "Time": t.time,
                    "Task": t.description,
                    "Frequency": t.frequency,
                    "Status": "✓ Done" if t.completed else "○ Pending"
                } for t in pet_tasks])

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.markdown("**⚠️ Scheduling Conflicts:**")
            for c in conflicts:
                st.warning(c)
        else:
            st.success("✅ No conflicts detected.")

# --- Filter View ---
st.divider()
st.subheader("🔍 Filter Tasks")
if owner.pets:
    filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
    filter_status = st.radio("Filter by status", ["All", "Pending", "Done"], horizontal=True)

    if st.button("Apply Filter"):
        if filter_pet == "All":
            tasks = owner.get_all_tasks()
        else:
            tasks = scheduler.filter_by_pet(filter_pet)

        if filter_status == "Pending":
            tasks = [t for t in tasks if not t.completed]
        elif filter_status == "Done":
            tasks = [t for t in tasks if t.completed]

        if tasks:
            st.table([{
                "Time": t.time,
                "Task": t.description,
                "Frequency": t.frequency,
                "Status": "✓ Done" if t.completed else "○ Pending"
            } for t in tasks])
        else:
            st.info("No tasks match that filter.")