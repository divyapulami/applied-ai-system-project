from pet_care_knowledge import PET_CARE_KNOWLEDGE


# ─────────────────────────────────────────────
# STEP 1: FIGURE OUT LIFE STAGE
# Is the pet a puppy, adult, or senior?
# ─────────────────────────────────────────────

def get_life_stage(species: str, age: int) -> str:
    species = species.lower()
    if species == "dog":
        if age < 1:
            return "puppy"
        elif age >= 8:
            return "senior dog"
        else:
            return "adult dog"
    elif species == "cat":
        if age < 1:
            return "kitten"
        elif age >= 10:
            return "senior cat"
        else:
            return "adult cat"
    else:
        return species


# ─────────────────────────────────────────────
# STEP 2: RETRIEVE MATCHING FACTS
# Search the knowledge base for facts that match
# the pet's species and life stage using keywords.
# No AI, no API, no internet needed.
# ─────────────────────────────────────────────

def is_age_appropriate(fact: str, life_stage: str) -> bool:
    """
    Returns False if a fact mentions an age stage that does NOT match the pet.
    For example: a 5-year-old dog should NOT see 'senior dog over 8 years old' facts.
    """
    fact_lower = fact.lower()

    puppy_terms   = ["puppy", "puppies", "kitten", "kittens"]
    senior_terms  = ["senior", "older than", "over 8", "over 10"]
    is_puppy_fact  = any(t in fact_lower for t in puppy_terms)
    is_senior_fact = any(t in fact_lower for t in senior_terms)

    # Exclude puppy/kitten facts if the pet is not in that life stage
    if is_puppy_fact and life_stage not in ("puppy", "kitten"):
        return False

    # Exclude senior facts if the pet is not in that life stage
    if is_senior_fact and "senior" not in life_stage:
        return False

    return True


def retrieve_facts(species: str, age: int, breed: str = "") -> list[str]:
    life_stage = get_life_stage(species, age)

    keywords = [species.lower(), life_stage.lower(), "all pets", "every pet", "pets need", "pets should"]

    if breed:
        for word in breed.lower().split():
            if len(word) > 3:
                keywords.append(word)

    breed_facts = []
    general_facts = []

    for fact in PET_CARE_KNOWLEDGE:
        fact_lower = fact.lower()

        # Skip facts meant for a different age stage
        if not is_age_appropriate(fact, life_stage):
            continue

        if breed and any(word in fact_lower for word in breed.lower().split() if len(word) > 3):
            breed_facts.append(fact)
        elif any(keyword in fact_lower for keyword in keywords):
            general_facts.append(fact)

    matched_facts = breed_facts + general_facts

    if not matched_facts:
        matched_facts = [
            "Pets need regular feeding, exercise, and veterinary checkups.",
            "Always provide fresh clean water for your pet.",
        ]

    return matched_facts[:10]


# ─────────────────────────────────────────────
# STEP 3: FORMAT THE RESULTS
# Group the retrieved facts into categories so
# they look like a proper care guide.
# No AI needed — we do the formatting ourselves.
# ─────────────────────────────────────────────

CATEGORIES = {
    "Feeding":   ["feed", "eat", "food", "meal", "diet", "water", "drink"],
    "Exercise":  ["exercise", "walk", "play", "active", "run"],
    "Grooming":  ["groom", "brush", "bath", "nail", "coat", "fur"],
    "Health":    ["vet", "vaccin", "flea", "tick", "health", "checkup", "spay", "neuter", "microchip", "dental", "teeth"],
}

def format_care_guide(pet_name: str, species: str, age: int, facts: list[str], breed: str = "") -> str:
    life_stage = get_life_stage(species, age)
    label = f"{breed} {life_stage}".strip() if breed else life_stage
    sections = {cat: [] for cat in CATEGORIES}
    other = []

    for fact in facts:
        placed = False
        for category, keywords in CATEGORIES.items():
            if any(kw in fact.lower() for kw in keywords):
                sections[category].append(fact)
                placed = True
                break
        if not placed:
            other.append(fact)

    lines = [f"### Care Guide for {pet_name} ({label})\n"]
    for category, items in sections.items():
        if items:
            lines.append(f"**{category}**")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

    if other:
        lines.append("**General Tips**")
        for item in other:
            lines.append(f"- {item}")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# CONFIDENCE SCORING
# Rates how relevant the retrieved facts are.
# Score is between 0.0 (low) and 1.0 (high).
#
# How it works:
#   - If the breed was specified and breed-specific facts were found → high confidence
#   - If only general species facts were found → medium confidence
#   - If very few facts were found → low confidence
# ─────────────────────────────────────────────

def compute_confidence(facts: list[str], breed: str) -> float:
    if not facts:
        return 0.0

    breed_words = [w for w in breed.lower().split() if len(w) > 3] if breed else []

    # Count how many of the returned facts are breed-specific
    breed_hits = 0
    if breed_words:
        for fact in facts:
            if any(word in fact.lower() for word in breed_words):
                breed_hits += 1

    total = len(facts)

    if breed_words:
        # Confidence = proportion of breed-specific facts found
        # Bonus: if we found at least 3 breed facts, confidence is high
        breed_ratio = breed_hits / total
        if breed_hits >= 3:
            return round(min(0.5 + breed_ratio * 0.5, 1.0), 2)
        elif breed_hits > 0:
            return round(0.4 + breed_ratio * 0.4, 2)
        else:
            # Breed given but no breed-specific facts found in knowledge base
            return round(min(total / 10 * 0.5, 0.5), 2)
    else:
        # No breed given — cap at 0.6 because general facts are less specific
        return round(min(total / 10 * 0.6, 0.6), 2)


# ─────────────────────────────────────────────
# FULL RAG PIPELINE (no AI required)
# retrieve → score confidence → format care guide
# ─────────────────────────────────────────────

def run_rag(pet_name: str, species: str, breed: str, age: int, api_key: str = "") -> tuple:
    facts = retrieve_facts(species, age, breed=breed)
    confidence = compute_confidence(facts, breed)
    guide = format_care_guide(pet_name, species, age, facts, breed=breed)
    return guide, facts, confidence
