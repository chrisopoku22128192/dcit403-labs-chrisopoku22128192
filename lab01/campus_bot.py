import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "groq/openai/gpt-oss-120b")
HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "facts.md")) as f:
    FACTS = f.read()

SYSTEM_PROMPT = f"""You are the Campus Info Bot for the Department of Computer Science.
You help new students find offices, opening hours and the right contact person.

RULES (performance measure):
- Answer only from the FACTS below. Never guess or use outside knowledge about the campus.
- If the answer is not in the FACTS, say you don't know. If an office in the
  FACTS handles that topic, refer the student to that office; otherwise refer
  them to the Department Office.
- Keep replies short: at most 3 sentences.
- Use earlier messages in the conversation to understand follow-up questions.

LIMITS (actuators):
- You can only reply with text.
- You cannot register students, book appointments, change records or send emails.
  If asked, say you cannot do that and tell the student who can.

FACTS (environment):
{FACTS}"""


def chat():
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Campus Info Bot. Type 'quit' to exit.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() == "quit":
            print("Bot: Goodbye!")
            break
        if not user:
            continue
        history.append({"role": "user", "content": user})
        try:
            resp = completion(model=MODEL, messages=history, temperature=0)
            reply = resp.choices[0].message.content or ""
        except Exception as e:
            reply = f"(Error contacting the model: {e})"
            history.pop()
        else:
            history.append({"role": "assistant", "content": reply})
        print(f"Bot: {reply}\n")


if __name__ == "__main__":
    chat()