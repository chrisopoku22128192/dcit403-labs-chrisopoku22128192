import os
import re
import sys
import json
import time
from dotenv import load_dotenv
from litellm import completion
from litellm.exceptions import BadRequestError
from tools import calculator, wiki_lookup

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "groq/openai/gpt-oss-120b")
EVIDENCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")

TOOLS = {"calculator": calculator, "wiki_lookup": wiki_lookup}

SYSTEM_PROMPT = """You are a helpful assistant for a trader at Makola Market.

You do NOT have function calling. Never call functions or tools directly.
Instead, write your chosen action as plain text, and the program will run it.

Available actions:
- calculator: evaluates arithmetic, e.g. 4*185 + 3*95
- wiki_lookup: returns a Wikipedia summary for a page title, e.g. Techiman
- finish: gives the final answer to the user

Always reply in exactly this plain-text format, one step at a time:

Thought: <your reasoning>
Action: calculator | wiki_lookup | finish
Action Input: <input for the action, or the final answer if finish>

Never do arithmetic yourself; always use the calculator.
Never write an Observation line; it will be given to you."""

FEW_SHOT = [
    {"role": "user", "content": "What is 12 * 7?"},
    {"role": "assistant", "content": "Thought: I need to multiply 12 by 7.\nAction: calculator\nAction Input: 12 * 7"},
    {"role": "user", "content": "Observation: 84"},
    {"role": "assistant", "content": "Thought: I have the answer.\nAction: finish\nAction Input: 12 * 7 is 84."},
]

FORMAT_HELP = ("Your reply did not follow the required format. Reply with exactly three lines: "
               "Thought: ..., Action: calculator | wiki_lookup | finish, Action Input: ...")

GARBLED_HELP = ("Your final answer was empty or garbled. "
                "Give a clear final answer in a full sentence.")

ACTION_RE = re.compile(r"Action:\s*(\w+)\s*\nAction Input:\s*(.*)", re.DOTALL)


def parse(text):
    m = ACTION_RE.search(text)
    if not m:
        return None, None
    return m.group(1).strip(), m.group(2).strip()


def first_step(text):
    idx = text.find("Action Input:")
    if idx == -1:
        return text
    start = idx + len("Action Input:")
    nxt = re.search(r"Thought:|Observation:|\nAction:", text[start:])
    if nxt:
        return text[:start + nxt.start()].rstrip()
    return text


def is_garbled(answer):
    chars = re.sub(r"\s", "", answer)
    if len(re.findall(r"[A-Za-z0-9]{2,}", answer)) < 3 or not chars:
        return True
    return len(re.findall(r"[A-Za-z0-9]", chars)) / len(chars) < 0.6


def recover_tool_call(error):
    s = str(error)
    start = s.find('{"error"')
    if start == -1:
        return None
    try:
        body, _ = json.JSONDecoder().raw_decode(s[start:])
        failed = body["error"].get("failed_generation", "")
    except Exception:
        return None
    try:
        call = json.loads(failed)
        args = call.get("arguments", {})
        value = next(iter(args.values()), "") if isinstance(args, dict) else args
        return f"Thought: (recovered from native tool call)\nAction: {call['name']}\nAction Input: {value}"
    except Exception:
        return failed or None


def call_model(messages):
    try:
        resp = completion(model=MODEL, messages=messages, stop=["Observation:"])
        return resp.choices[0].message.content or ""
    except BadRequestError as e:
        recovered = recover_tool_call(e)
        if recovered:
            return recovered
        raise


def run_tool(action, action_input):
    try:
        return TOOLS[action](action_input)
    except Exception as e:
        return f"Error: tool failed ({e})"


def run_agent(question, max_steps=6, trace_file=None):
    messages = ([{"role": "system", "content": SYSTEM_PROMPT}]
                + FEW_SHOT
                + [{"role": "user", "content": question}])
    trace = [f"Question: {question}", f"Model: {MODEL}", ""]
    answer = None

    for step in range(1, max_steps + 1):
        reply = first_step(call_model(messages).strip())
        trace.append(f"--- Step {step} ---")
        trace.append(reply)
        messages.append({"role": "assistant", "content": reply})

        action, action_input = parse(reply)

        if action is None:
            observation = FORMAT_HELP
        elif action == "finish":
            if is_garbled(action_input):
                observation = GARBLED_HELP
            else:
                answer = action_input
                trace.append(f"\nFinal answer: {answer}")
                break
        elif action in TOOLS:
            observation = run_tool(action, action_input)
        else:
            observation = (f"Unknown action '{action}'. "
                           "Use one of: calculator, wiki_lookup, finish.")

        trace.append(f"Observation: {observation}")
        messages.append({"role": "user", "content": f"Observation: {observation}"})
        time.sleep(1)
    else:
        trace.append(f"\nStopped: reached max_steps ({max_steps}) without finishing.")

    text = "\n".join(trace)
    print(text)
    print("=" * 60)
    if trace_file:
        os.makedirs(EVIDENCE, exist_ok=True)
        with open(os.path.join(EVIDENCE, trace_file), "w") as f:
            f.write(text + "\n")
    return answer


QUESTIONS = [
    "I have GHS 1,200. I want 4 bags of rice at GHS 185 each and 3 gallons of oil at GHS 95 each. How much will I have left?",
    "What is the capital of the Bono East Region? If I sell 25 bags of rice there at GHS 190 each, how much will I earn?",
    "Which region is Techiman the capital of, and how much do 12 crates of eggs cost at GHS 65 each?",
    "Look up the Wikipedia page for the Kwame Asante Plantain Exchange of Ghana.",
    "Say good morning to me in Twi.",
    "rice 4 185 oil 3 95 i got 1200 how much left??",
]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        run_agent(QUESTIONS[n - 1], trace_file=f"trace_{n}.txt")
    else:
        for n, q in enumerate(QUESTIONS, start=1):
            run_agent(q, trace_file=f"trace_{n}.txt")
            time.sleep(3)