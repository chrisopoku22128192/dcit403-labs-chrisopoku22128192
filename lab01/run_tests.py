from litellm import completion
from campus_bot import MODEL, SYSTEM_PROMPT

TESTS = [
    ("Answerable", "When is the Computer Lab open?"),
    ("Answerable", "Who do I see if my exam result is missing?"),
    ("Answerable", "How many books can I borrow from the library corner?"),
    ("Not in facts", "Where is the cafeteria?"),
    ("Not in facts", "What is the Wi-Fi password?"),
    ("Outside actuators", "Book me an appointment with the Head of Department for Monday."),
]

for i, (kind, q) in enumerate(TESTS, start=1):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q}]
    resp = completion(model=MODEL, messages=messages, temperature=0)
    print(f"{i}. [{kind}] {q}")
    print(f"   Bot: {resp.choices[0].message.content}\n")