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
The scheduler detects conflicts by checking for exact time string matches between
tasks for the same pet. This means two tasks at "09:00" are flagged, but a task
at "09:00" and one at "09:15" are not — even if the first one takes 30 minutes.
This is reasonable for a pet care app because most tasks (feeding, giving
medication, a quick walk) are treated as point-in-time events, not time blocks.
Exact-match detection catches the most common real-world mistake — accidentally
scheduling two things at the same time — without needing complex interval math.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI at every phase of the project. During design, I described my four
classes in plain English and asked Copilot to generate a Mermaid.js UML diagram,
which helped me spot a missing Owner→Pet relationship before writing any code.
During implementation, I used Agent Mode to scaffold method stubs from the UML
so I could focus on logic instead of boilerplate. For the algorithms in Phase 4,
I asked Copilot how to use a lambda with sorted() for time-based sorting and how
to use timedelta for recurring task dates. For testing, I used the Generate Tests
smart action as a first draft and then reviewed each test manually.

The most helpful prompts were specific and file-grounded — using #file:pawpal_system.py
gave Copilot real context. Questions like "given my current implementation, how
should the Scheduler retrieve tasks from the Owner?" worked much better than
vague ones like "how do I build a scheduler?"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
When I asked Copilot to generate the conflict detection method, it produced a
version that raised a ValueError when a conflict was found. I did not accept
this because the project required a warning, not a crash — raising an exception
would force the Streamlit UI to wrap every task addition in a try/except block,
which leaks scheduling logic into the frontend. I traced the execution path from
app.py through to the Scheduler to confirm the UI could not recover gracefully
from an exception, then rewrote the method to return a warning string instead.
The UI could then display it with st.warning() cleanly.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested five core behaviors:
- Task completion: calling mark_complete() sets the task's completed field to True
- Task addition: add_task() increases the pet's task count by exactly one
- Sorting: tasks added out of order are returned in chronological HH:MM order
- Recurrence: marking a daily task complete creates a new task for the next day
- Conflict detection: two tasks at the same time return a warning string, not an exception

These tests mattered because they each cover a distinct failure mode — wrong
state mutation, silent data loss, sort instability, off-by-one date math, and
incorrect error handling — rather than testing the same path twice.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
The main happy paths and most likely edge cases are covered. If I had more time
I would test: a pet with zero tasks, a task scheduled at midnight (00:00) to
check string sort boundary behavior, weekly recurrence (only daily is currently
tested), and conflict detection across two different pets rather than just the
same pet.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The CLI-first workflow was the best decision I made. Building and verifying all
logic through main.py before touching app.py meant I was never debugging backend
logic through a UI. Every time the terminal printed a clean sorted schedule I had
real confidence before wiring anything to Streamlit.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would replace the HH:MM string format for task times with Python datetime.time
objects. String comparison works for zero-padded times but breaks silently if a
user types "9:00" instead of "09:00" — sorting and conflict detection both fail
without any error. Using datetime.time makes all comparisons correct by
construction and would only require a small change to the Task dataclass and
input validation in app.py.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
AI is most useful as a fast first draft, not a final answer. Every piece of
AI-generated code in this project needed human review to be production-quality —
whether that meant changing an exception to a warning, choosing a better type,
or tightening a test that passed but did not verify the right thing. The lead
architect role is not about writing every line; it is about knowing which lines
are wrong and why.
