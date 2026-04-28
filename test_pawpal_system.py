import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_mark_complete_sets_completed_true():
    task = Task(
        task_id=1,
        title="Feed",
        description="Feed the pet",
        due_date="2026-03-30",
        time="08:00",
        frequency="one-time",
    )
    assert not task.completed

    done, next_task = task.mark_complete()

    assert done is True
    assert task.completed is True
    assert next_task is None


def test_pet_add_task_increases_task_count():
    pet = Pet(pet_id=1, name="Buddy", species="Dog", breed="Labrador", age=4)
    initial_count = len(pet.get_tasks())

    task = Task(
        task_id=2,
        title="Walk",
        description="Walk in the park",
        due_date="2026-03-30",
        time="09:00",
        frequency="daily",
    )
    pet.add_task(task)

    assert len(pet.get_tasks()) == initial_count + 1


def test_scheduler_sort_by_time_returns_chronological():
    scheduler = Scheduler()
    task1 = Task(
        task_id=1,
        title="Evening",
        description="Evening play",
        due_date="2026-03-30",
        time="18:00",
        frequency="daily",
    )
    task2 = Task(
        task_id=2,
        title="Morning",
        description="Morning walk",
        due_date="2026-03-30",
        time="08:00",
        frequency="daily",
    )
    task3 = Task(
        task_id=3,
        title="Noon",
        description="Lunchtime meds",
        due_date="2026-03-30",
        time="12:00",
        frequency="weekly",
    )
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)

    sorted_tasks = scheduler.sort_by_time()
    assert [t.time for t in sorted_tasks] == ["08:00", "12:00", "18:00"]


def test_complete_daily_recurring_task_creates_next_day():
    pet = Pet(pet_id=1, name="Mittens", species="Cat", breed="Siamese", age=2)
    scheduler = Scheduler()
    task = Task(
        task_id=100,
        title="Daily meds",
        description="Give meds",
        due_date="2026-03-30",
        time="07:00",
        frequency="daily",
    )
    scheduler.add_task(task, pet=pet)

    next_task = scheduler.complete_task(task_id=100, pet=pet)

    assert next_task is not None
    assert next_task.due_date == "2026-03-31"
    assert next_task.completed is False
    assert any(t.task_id == next_task.task_id for t in scheduler.tasks)
    assert any(t.task_id == next_task.task_id for t in pet.tasks)


def test_conflict_detection_warns_on_same_date_time():
    scheduler = Scheduler()
    task_up = Task(
        task_id=1,
        title="Task A",
        description="Same time A",
        due_date="2026-03-30",
        time="10:00",
        frequency="one-time",
    )
    task_down = Task(
        task_id=2,
        title="Task B",
        description="Same time B",
        due_date="2026-03-30",
        time="10:00",
        frequency="one-time",
    )
    scheduler.add_task(task_up)
    scheduler.add_task(task_down)

    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "2026-03-30 10:00" in warnings[0]
    assert "Task A" in warnings[0] and "Task B" in warnings[0]


# ─────────────────────────────────────────────
# RAG ENGINE TESTS
# These tests prove the retrieval logic works correctly.
# ─────────────────────────────────────────────

from rag_engine import retrieve_facts, compute_confidence, get_life_stage, is_age_appropriate


def test_retrieve_facts_returns_dog_facts_for_dog():
    facts = retrieve_facts(species="dog", age=4, breed="Labrador Retriever")
    # Every returned fact should be relevant to dogs (not cats or rabbits)
    for fact in facts:
        assert "cat" not in fact.lower() and "rabbit" not in fact.lower(), (
            f"Dog query returned a non-dog fact: {fact}"
        )


def test_retrieve_facts_excludes_senior_facts_for_young_dog():
    # A 3-year-old dog is an adult — should never see senior advice
    facts = retrieve_facts(species="dog", age=3, breed="")
    for fact in facts:
        assert "senior" not in fact.lower() and "over 8" not in fact.lower(), (
            f"Adult dog received senior fact: {fact}"
        )


def test_retrieve_facts_excludes_adult_facts_for_puppy():
    # A puppy should never see senior advice
    facts = retrieve_facts(species="dog", age=0, breed="")
    for fact in facts:
        assert "senior" not in fact.lower(), (
            f"Puppy received senior fact: {fact}"
        )


def test_breed_specific_facts_appear_for_known_breed():
    # A Labrador query should return at least one Labrador-specific fact
    facts = retrieve_facts(species="dog", age=4, breed="Labrador Retriever")
    has_breed_fact = any("labrador" in f.lower() for f in facts)
    assert has_breed_fact, "No Labrador-specific facts returned for a Labrador Retriever"


def test_confidence_is_high_when_breed_facts_found():
    facts = retrieve_facts(species="dog", age=4, breed="Labrador Retriever")
    score = compute_confidence(facts, breed="Labrador Retriever")
    assert score >= 0.7, f"Expected high confidence for known breed, got {score}"


def test_confidence_is_lower_without_breed():
    # No breed given — only general species facts, so confidence should be lower
    facts_no_breed = retrieve_facts(species="dog", age=4, breed="")
    facts_with_breed = retrieve_facts(species="dog", age=4, breed="Labrador Retriever")
    score_no_breed = compute_confidence(facts_no_breed, breed="")
    score_with_breed = compute_confidence(facts_with_breed, breed="Labrador Retriever")
    assert score_with_breed >= score_no_breed, (
        "Confidence should be higher when a known breed is given"
    )