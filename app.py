import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State: initialize Owner and Scheduler once ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# --- Owner Setup ---
st.subheader("👤 Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=owner.name or "Jordan")
with col2:
    owner_email = st.text_input("Email", value=owner.email or "jordan@email.com")

if st.button("Save Owner"):
    owner.name = owner_name
    owner.email = owner_email
    st.success(f"Owner set to {owner.name}")

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
    existing = [p.name.lower() for p in owner.pets]
    if pet_name.lower() in existing:
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, age=age))
        st.success(f"{pet_name} the {species} added!")

if owner.pets:
    st.write("**Your pets:**", ", ".join(p.name for p in owner.pets))

st.divider()

# --- Add a Task ---
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
        new_task = Task(
            description=task_desc,
            time=task_time,
            frequency=frequency,
            due_date=date.today()
        )
        pet.add_task(new_task)

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for c in conflicts:
                st.warning(f"⚠️ {c}")
        else:
            st.success(f"Task '{task_desc}' added for {selected_pet} at {task_time}.")

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
                rows = []
                for t in pet_tasks:
                    rows.append({
                        "Time": t.time,
                        "Task": t.description,
                        "Frequency": t.frequency,
                        "Done": "✓" if t.completed else "○"
                    })
                st.table(rows)

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.markdown("**⚠️ Conflicts detected:**")
            for c in conflicts:
                st.warning(c)
        else:
            st.success("✅ No scheduling conflicts.")