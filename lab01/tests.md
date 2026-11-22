# Lab 1 Tests: Campus Info Bot

Model: groq/openai/gpt-oss-120b, temperature 0

| # | Type | Question | Response (summary) | Result | Why |
|---|------|----------|--------------------|--------|-----|
| 1 | Answerable | When is the Computer Lab open? | Mon to Sat, 7:00 am to 9:00 pm | Pass | Matches fact 4 |
| 2 | Answerable | Who do I see if my exam result is missing? | Mr. Kofi Boateng, Room 106, Block C | Pass | Matches fact 3 |
| 3 | Answerable | How many books can I borrow? | Up to 3 books | Pass | Matches fact 7 (left out "2 weeks") |
| 4 | Not in facts | Where is the cafeteria? | Doesn't know; refers to Department Office | Pass | No guessing; correct fallback |
| 5 | Not in facts | What is the Wi-Fi password? | Doesn't know; refers to **Department Office** | **Fail** | Fact 6 says the IT Help Desk handles Wi-Fi; wrong contact |
| 6 | Outside actuators | Book me an appointment with the HOD | Can't book; refers to Department Office | Pass | Stays within actuators; matches fact 2 |

## Fix
**Failure:** Test 5 sent the student to the Department Office although the IT Help Desk handles Wi-Fi.
The rule "if unsure, refer to the Department Office" was applied too literally.

**Change to system prompt:**
- Before: "If the answer is not in the FACTS, say you don't know and refer the student to the Department Office."
- After: "If the answer is not in the FACTS, say you don't know. If an office in the FACTS handles that topic, refer the student to that office; otherwise refer them to the Department Office."

**Re-run of Test 5:** "I don't have that information. Please contact the IT Help Desk in Block D, Room 201 for Wi-Fi password assistance." **Pass**