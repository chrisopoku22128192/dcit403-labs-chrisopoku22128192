# PEAS: Campus Info Bot

| PEAS | Campus Info Bot |
|------|-----------------|
| Performance | Correct answers about offices, hours and contacts; answers only from the facts given; says "I don't know" and refers to the department office when unsure; never pretends to register, book or change anything; short replies |
| Environment | New students on a terminal chat; a facts sheet of department offices, hours and contacts; the department office as fallback |
| Actuators | Send a text reply; refer the student to the department office |
| Sensors | The student's typed messages; the conversation history; the facts sheet it is given |

## Environment properties

| Property | Classification | Reason |
|----------|----------------|--------|
| Observable | Partially | It sees messages, not the student's records, timetable or intent |
| Deterministic | Stochastic | Students ask unexpected questions in unexpected ways |
| Episodic | Sequential | Earlier turns matter, e.g. "where is it?" refers to an office named before |
| Static | Static | Facts do not change during a chat |
| Discrete | Discrete | The chat moves in separate turns of text |
| Agents | Single-agent | Only the student interacts with it; no competing agent |