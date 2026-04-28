import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler
from rag_engine import run_rag

# Initialize persistent app state once
if "owner_obj" not in st.session_state:
    st.session_state.owner_obj = Owner(owner_id=1, name="Jordan")

if "scheduler_obj" not in st.session_state:
    st.session_state.scheduler_obj = Scheduler()

if "task_id_counter" not in st.session_state:
    st.session_state.task_id_counter = 1000

owner: Owner = st.session_state.owner_obj
scheduler: Scheduler = st.session_state.scheduler_obj

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")


st.markdown("""This demo uses your scheduler logic (sorting, filtering, recurring and conflict detection).""")

st.subheader("Owner & Pets")
with st.form("pet_form", clear_on_submit=True):
    name_input = st.text_input("Owner name", value=owner.name)
    pet_name = st.text_input("New pet name", "Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", "")
    age = st.number_input("Age", min_value=0, max_value=30, value=1)
    add_pet = st.form_submit_button("Add Pet")

    if add_pet:
        owner.name = name_input or owner.name
        next_pet_id = (max([p.pet_id for p in owner.pets]) + 1) if owner.pets else 101
        new_pet = Pet(pet_id=next_pet_id, name=pet_name, species=species, breed=breed, age=int(age))
        owner.add_pet(new_pet)
        st.success(f"Pet '{new_pet.name}' added")

if owner.get_pets():
    st.table(
        [{"Pet ID": p.pet_id, "Name": p.name, "Species": p.species, "Breed": p.breed, "Age": p.age} for p in owner.get_pets()]
    )
else:
    st.info("No pets yet. Add one to start scheduling.")

st.divider()

st.subheader("Task input & schedule")
if not owner.get_pets():
    st.warning("Add at least one pet before creating tasks")
else:
    pet_choices = {p.name: p for p in owner.get_pets()}
    selected_pet_name = st.selectbox("Assign task to pet", list(pet_choices.keys()))
    selected_pet = pet_choices[selected_pet_name]

    task_title = st.text_input("Task title", "Morning walk")
    task_description = st.text_input("Description", "")
    task_time = st.time_input("Time", value=None)
    frequency = st.selectbox("Frequency", ["one-time", "daily", "weekly"])

    if st.button("Add scheduled task"):
        st.session_state.task_id_counter += 1
        next_id = st.session_state.task_id_counter
        due = date.today().isoformat()
        new_task = Task(
            task_id=next_id,
            title=task_title,
            description=task_description,
            due_date=due,
            time=task_time.strftime("%H:%M"),
            frequency=frequency,
        )
        scheduler.add_task(new_task, pet=selected_pet)
        st.success(f"Task '{task_title}' added for {selected_pet.name} at {new_task.time}")

    if scheduler.tasks:
        st.markdown("### All tasks")
        st.table([
            {
                "Task ID": t.task_id,
                "Title": t.title,
                "Pet": "Buddy" if t in owner.pets[0].tasks else ("Mittens" if len(owner.pets) > 1 and t in owner.pets[1].tasks else "Unknown"),
                "Due date": t.due_date,
                "Time": t.time,
                "Frequency": t.frequency,
                "Done": t.completed,
            }
            for t in scheduler.tasks
        ])

        st.markdown("### Sorted tasks")
        sorted_tasks = scheduler.sort_by_time()
        st.table([
            {"Time": t.time, "Title": t.title, "Pet": "Buddy" if t in owner.pets[0].tasks else ("Mittens" if len(owner.pets) > 1 and t in owner.pets[1].tasks else "Unknown"), "Done": t.completed}
            for t in sorted_tasks
        ])

        st.markdown("### Pending tasks")
        pending = scheduler.filter_by_completion(False)
        if pending:
            st.table([{"Time": t.time, "Title": t.title, "Pet": selected_pet_name, "Due": t.due_date} for t in pending])
        else:
            st.success("No pending tasks")

        st.markdown(f"### Tasks for {selected_pet.name}")
        pet_tasks = scheduler.filter_by_pet_name(selected_pet.name, owner)
        if pet_tasks:
            st.table([{"Time": t.time, "Title": t.title, "Due": t.due_date, "Done": t.completed} for t in pet_tasks])
        else:
            st.info("No tasks for this pet")

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No task conflicts found")

    else:
        st.info("No scheduled tasks yet.")

st.divider()

# ── AI CARE ADVISOR (RAG) ──────────────────────────────────────────────────
# Flow (matches your architecture diagram):
#   User picks pet → RAG retrieves facts → Claude generates schedule → User reviews
# ──────────────────────────────────────────────────────────────────────────
st.subheader("🐾 AI Care Advisor")
st.markdown("Ask the AI for a personalized care schedule based on your pet's info.")

if not owner.get_pets():
    st.info("Add a pet above to use the AI Care Advisor.")
else:
    ai_pet_choices = {p.name: p for p in owner.get_pets()}
    ai_selected_name = st.selectbox("Select a pet for AI advice", list(ai_pet_choices.keys()), key="ai_pet_select")
    ai_pet = ai_pet_choices[ai_selected_name]

    # Clear stored results when the user switches to a different pet
    if st.session_state.get("rag_last_pet") != ai_pet.pet_id:
        st.session_state["rag_results"] = None
        st.session_state["rag_last_pet"] = ai_pet.pet_id

    if st.button("Get AI Care Advice"):
        with st.spinner(f"Searching care knowledge for {ai_pet.name}..."):
            schedule_text, retrieved_facts, confidence = run_rag(
                pet_name=ai_pet.name,
                species=ai_pet.species,
                breed=ai_pet.breed,
                age=ai_pet.age,
            )
            st.session_state["rag_results"] = {
                "pet_id": ai_pet.pet_id,
                "schedule": schedule_text,
                "facts": retrieved_facts,
                "confidence": confidence,
            }

    # Show results only if they belong to the currently selected pet
    result = st.session_state.get("rag_results")
    if result and result["pet_id"] == ai_pet.pet_id:
        confidence = result["confidence"]

        # Show confidence score with a colour indicator
        if confidence >= 0.75:
            st.success(f"Confidence Score: {confidence} — High match. Breed-specific facts found.")
        elif confidence >= 0.4:
            st.warning(f"Confidence Score: {confidence} — Medium match. Try entering the full breed name for better results.")
        else:
            st.error(f"Confidence Score: {confidence} — Low match. This breed may not be in the knowledge base yet.")

        st.markdown("#### Facts Retrieved from Knowledge Base")
        st.caption("These are the care tips matched to your pet:")
        for fact in result["facts"]:
            st.markdown(f"- {fact}")
        st.markdown("#### Care Guide")
        st.success(result["schedule"])
        st.info("Review the guide above, then manually add the tasks you want using the Task input section above.")

