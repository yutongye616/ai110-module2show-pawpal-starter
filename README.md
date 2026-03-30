# 🐾 PawPal+

A smart pet care management system built with Python OOP and Streamlit.
PawPal+ helps pet owners track daily routines — feedings, walks, medications,
and appointments — using algorithmic scheduling logic to organize and prioritize tasks.

---

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank">
  <img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App'
  width='' alt='PawPal App' class='center-block' />
</a>

---

## ✨ Features

- **Owner & pet management** — create an owner, add multiple pets, and manage
  them all in one place with persistent session state
- **Task scheduling** — assign care tasks to individual pets with a time,
  description, and frequency (once / daily / weekly)
- **Sorting by time** — the Scheduler automatically sorts all tasks into
  chronological order using Python's `sorted()` with a lambda key on HH:MM strings
- **Filtering** — filter the schedule by pet name or completion status to focus
  on exactly what needs attention
- **Conflict warnings** — the Scheduler scans each pet's tasks for exact time
  matches and surfaces a plain-language warning in the UI via `st.warning()`
  rather than crashing
- **Daily recurrence** — marking a daily or weekly task complete automatically
  generates the next occurrence using Python's `timedelta`

---

## 🗂 Project Structure
```
pawpal_system.py   — backend logic (Owner, Pet, Task, Scheduler classes)
app.py             — Streamlit UI
main.py            — CLI demo script for verifying backend logic
tests/
  test_pawpal.py   — automated pytest suite
uml_final.png      — final system architecture diagram
reflection.md      — design decisions and AI collaboration notes
```

---

## 🚀 How to Run
```bash
# Install dependencies
pip install streamlit pytest

# Run the app
streamlit run app.py

# Run the CLI demo
python main.py
```

---

## Smarter Scheduling

PawPal+ includes four algorithmic features in the `Scheduler` class:

**Sorting by time** — tasks are sorted chronologically using `sorted()` with a
lambda key on the HH:MM time string so owners always see their day in order
regardless of the order tasks were added.

**Filtering** — tasks can be filtered by pet name or completion status, letting
owners focus on one animal or see only what still needs to be done.

**Recurring tasks** — when a daily or weekly task is marked complete, the
Scheduler automatically generates a new Task for the next occurrence using
`timedelta`. Daily tasks roll forward 1 day, weekly tasks roll forward 7 days.

**Conflict detection** — the Scheduler scans each pet's tasks for exact time
matches and returns a plain-language warning string rather than crashing,
so the UI can surface the conflict gracefully.

---

## Testing PawPal+
```bash
python -m pytest
```

The test suite covers:

- Task completion toggling
- Task addition increasing pet task count
- Sorting returning chronological order
- Conflict detection flagging duplicate times
- Recurrence generating tomorrow's task after mark complete
- Pet with no tasks returning empty list without crashing
- Filter by pet name returning correct tasks
- Filter by status returning only matching tasks
- One-time tasks not generating a next occurrence

**Confidence level: ⭐⭐⭐⭐ (4/5)**

Happy paths and the most common edge cases are covered. Remaining gaps:
weekly recurrence, midnight boundary sorting, and cross-pet conflict detection.

---

## 🏗 System Architecture

See `uml_final.png` for the full class diagram. The four core classes are:

- `Task` — dataclass representing a single care activity
- `Pet` — dataclass storing pet details and a list of tasks
- `Owner` — manages multiple pets and exposes a flat task list
- `Scheduler` — all algorithmic logic: sorting, filtering, conflict detection,
  and recurring task generation