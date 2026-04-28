# Model Card — PawPal+ RAG Care Advisor

---

## System Overview

**System name:** PawPal+ AI Care Advisor
**Type:** Retrieval-Augmented Generation (RAG) system — keyword-based retrieval with deterministic formatting
**Base project:** PawPal+ pet care task scheduler (built in Modules 1–3)
**Author:** Divya Pulami — CodePath Applied AI Systems

PawPal+ AI Care Advisor retrieves breed-specific, age-appropriate pet care facts from a curated knowledge base and formats them into a structured care guide. It does not use a live LLM or any external API — all retrieval and formatting runs locally.

---

## Intended Use

**Primary use:** Helping beginner pet owners get quick, breed-specific care guidance for feeding, exercise, grooming, and health routines.

**Intended users:** Pet owners who are new to caring for a specific breed and want a starting point for building a care routine.

**Not intended for:**
- Replacing professional veterinary advice or diagnosis
- Medical treatment decisions
- Pets with known health conditions that require specialized care

---

## Knowledge Base

The system retrieves facts from `pet_care_knowledge.py`, a manually curated list of 100+ facts I wrote myself. It covers:

| Species | Breeds Covered |
|---|---|
| Dog | Labrador Retriever, Golden Retriever, German Shepherd, French Bulldog, Poodle, Chihuahua, Beagle, Husky, Shih Tzu, Dachshund, Border Collie |
| Cat | Persian, Siamese, Maine Coon, Bengal, Ragdoll, British Shorthair, Sphynx |
| Rabbit | Holland Lop, Lionhead, Flemish Giant, Mini Rex |
| Other | Guinea Pig, Hamster, Parrot/Budgie/Cockatiel/African Grey |

**Knowledge source:** Written by me (a student) based on general pet care research. Not reviewed or verified by a licensed veterinarian.

---

## How It Works

1. User enters a pet's name, species, breed, and age
2. `retrieve_facts()` searches the knowledge base using keyword matching on species, breed name, and life stage (puppy / adult / senior)
3. `is_age_appropriate()` filters out facts that don't match the pet's age stage
4. `compute_confidence()` scores how many breed-specific facts were found (0.0–1.0)
5. `format_care_guide()` groups the facts into Feeding, Exercise, Grooming, and Health sections

---

## Confidence Scoring

The system rates its own reliability for each query:

| Score | Label | Meaning |
|---|---|---|
| ≥ 0.75 | High | Breed found in knowledge base with 4+ specific facts |
| 0.40–0.74 | Medium | Only general species facts found; try entering the full breed name |
| < 0.40 | Low | Breed not in knowledge base |

Known breeds from the table above consistently score **0.75**. Queries with no breed entered score **0.6**.

---

## Limitations and Biases

### Knowledge bias
The knowledge base reflects my own research and understanding, which means:
- **Popular Western breeds are overrepresented.** Labrador Retrievers and German Shepherds have more detailed coverage than less common breeds.
- **Dogs and cats have significantly more coverage than rabbits, guinea pigs, hamsters, and birds.** If someone asks about an exotic pet, results will be sparse.
- **Facts are generalizations.** All Huskies get the same advice regardless of individual health history, weight, or living situation.

### Language and input bias
- The keyword matching system requires breed names to be spelled exactly as written in the knowledge base. A user typing "lab" will not match "Labrador Retriever" facts.
- The system has no understanding of context — it cannot tell the difference between a healthy pet and a sick one.

### Age threshold bias
- I define "senior dog" as age 8 and above, and "senior cat" as age 10 and above. These are averages — large dog breeds age faster and small breeds often live longer. The system does not account for breed-specific aging.

### Not medically verified
All facts were written by me, not a licensed veterinarian. Some facts may be oversimplified or incomplete for specific situations.

---

## Ethical Considerations

### Risk of over-reliance
A pet owner could follow the system's advice without consulting a vet, especially for health reminders. To reduce this risk, the app includes a disclaimer: *"Review the guide above, then manually add the tasks you want."* In a production version, I would add a more prominent disclaimer stating that the advice does not replace professional veterinary care.

### No personal data collected
The system does not store, log, or transmit any user data. All pet information entered into the app exists only in Streamlit's session state and is cleared when the browser tab is closed.

### Transparency
The app shows users exactly which facts were retrieved from the knowledge base before displaying the formatted care guide. This lets users verify where the advice came from and spot anything that doesn't apply to their specific pet.

---

## Testing Results

I ran 11 automated tests using pytest — 5 for the scheduler logic and 6 for the RAG retrieval system.

**All 11 tests passed.**

| Test | What it checks | Result |
|---|---|---|
| `test_task_mark_complete_sets_completed_true` | Task completion sets flag correctly | Passed |
| `test_pet_add_task_increases_task_count` | Adding a task increases pet's task count | Passed |
| `test_scheduler_sort_by_time_returns_chronological` | Tasks sort in time order | Passed |
| `test_complete_daily_recurring_task_creates_next_day` | Daily tasks auto-create next occurrence | Passed |
| `test_conflict_detection_warns_on_same_date_time` | Two tasks at same time get flagged | Passed |
| `test_retrieve_facts_returns_dog_facts_for_dog` | Dog query returns no cat/rabbit facts | Passed |
| `test_retrieve_facts_excludes_senior_facts_for_young_dog` | Adult dog gets no senior advice | Passed |
| `test_retrieve_facts_excludes_adult_facts_for_puppy` | Puppy gets no senior advice | Passed |
| `test_breed_specific_facts_appear_for_known_breed` | Labrador query returns Labrador-specific facts | Passed |
| `test_confidence_is_high_when_breed_facts_found` | Known breed scores ≥ 0.7 confidence | Passed |
| `test_confidence_is_lower_without_breed` | No-breed query scores lower than breed query | Passed |

### Bug found during testing
While testing confidence scores, I noticed every breed was returning exactly **0.70** instead of the expected **0.75**. Debugging revealed that the fact `"Persian cat is prone to kidney disease — annual vet bloodwork is recommended after age 4"` was being excluded by the age filter because `"after age"` was in my list of senior-indicator terms. The fix was to remove that overly broad term. This is a good example of how a single word in a filter list can silently produce wrong results without throwing any error.

---

## AI Collaboration

### How I used AI
I used Claude (via Claude Code) throughout this project for step-by-step implementation guidance, debugging, and code generation. The most helpful uses were:
- Designing the RAG pipeline structure and explaining each component in simple terms
- Writing the confidence scoring formula
- Debugging the confidence score bug by analyzing the exact hit counts per breed in the terminal
- Writing the test suite for the RAG layer

### Instance where AI gave a helpful suggestion
When I was stuck trying to get both the Anthropic and Google Gemini APIs to work (both had billing or quota issues), Claude suggested removing the LLM generation step entirely and replacing it with a deterministic formatter. I was skeptical because I thought the AI generation step was the whole point. But Claude explained that retrieval quality is what makes RAG valuable, and a well-formatted retrieval result is still genuinely useful. That suggestion turned a blocked project into a working, reliable, and completely free system.

### Instance where AI gave a flawed suggestion
When switching from Anthropic to Google Gemini, Claude suggested using `gemini-1.5-flash` as the model name. This caused a `404 Not Found` error because the model wasn't available in the installed version of the library. Claude then switched to `gemini-2.0-flash`, which fixed the error — but that model hit the free tier quota almost immediately during testing. Both suggestions assumed a working, properly funded API setup that I didn't have. The real solution — removing the API entirely — wasn't suggested until I explicitly pushed back and asked for a fundamentally different approach. This taught me that AI assistants tend to suggest the most common path first, and sometimes you have to redirect them to think outside that path.
