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

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes four algorithmic features in the `Scheduler` class:

**Sorting by time**: Tasks are sorted chronologically using Python's `sorted()`
with a lambda key on the HH:MM time string, so owners always see their day
in order regardless of the order tasks were added.

**Filtering**: Tasks can be filtered by pet name or completion status, letting
owners focus on one animal or see only what still needs to be done.

**Recurring tasks**: When a daily or weekly task is marked complete, the
Scheduler automatically generates a new Task for the next occurrence using
Python's `timedelta` — daily tasks roll forward 1 day, weekly tasks roll
forward 7 days.

**Conflict detection**: The Scheduler scans each pet's tasks for exact time
matches and returns a plain-language warning string rather than crashing,
so the UI can surface the conflict gracefully.v