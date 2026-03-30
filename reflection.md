# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design centered on four classes with clearly separated responsibilities:

- **Task**: A dataclass holding a single pet care activity — its description, scheduled time (HH:MM string), frequency ("once", "daily", "weekly"), and a completion boolean. It is a pure data container with no scheduling logic of its own.
- **Pet**: A dataclass storing a pet's name and species, along with a list of Task objects. It exposes methods to add tasks and retrieve its task list.
- **Owner**: Acts as the top-level registry. It holds a list of Pet objects and provides a method to retrieve all tasks across all pets in a flat list, making it easy for the Scheduler to consume.
- **Scheduler**: The "brain" of the system. It holds a reference to an Owner and is responsible for all algorithmic work — sorting, filtering, conflict detection, and recurring task generation. No business logic lives in the other classes.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design changed in one meaningful way. In the initial skeleton, `mark_complete()` was a simple boolean toggle on Task. During Phase 4, when implementing recurring tasks, I realized this method needed to do more: when a daily or weekly task is marked complete, it should automatically create and return a new Task scheduled for the next occurrence. This meant `mark_complete()` could no longer be a one-liner on a passive dataclass — I moved the recurrence logic into the Scheduler's `mark_task_complete()` method instead, keeping Task itself simple and letting the Scheduler handle the complexity. This separation made the recurrence logic easier to test in isolation.

---

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
