import os
import csv
import json
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "groq/openai/gpt-oss-120b")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "pharmacy_stock.csv")


def check_stock(item, strength=""):
    with open(DATA, newline="") as f:
        rows = list(csv.DictReader(f))
    rows = [r for r in rows if item.lower() in r["item"].lower()]
    if strength:
        rows = [r for r in rows if strength.lower() in r["strength"].lower()]
    return rows


TOOLS = {"check_stock": check_stock}

tool_schemas = [{
    "type": "function",
    "function": {
        "name": "check_stock",
        "description": ("Look up pharmacy stock for a medicine. Returns matching rows with item, "
                        "strength, form, quantity, unit_price_ghs and expiry_date. Use it for any "
                        "question about availability, quantity, price or expiry."),
        "parameters": {
            "type": "object",
            "properties": {
                "item": {"type": "string", "description": "Medicine name, e.g. amoxicillin"},
                "strength": {"type": "string", "description": "Optional strength, e.g. 500mg"},
            },
            "required": ["item"],
        },
    },
}]

question = "Do we have amoxicillin 500mg?"
messages = [
    {"role": "system", "content": "You are a pharmacy stock assistant. Answer only from tool results."},
    {"role": "user", "content": question},
]

resp = completion(model=MODEL, messages=messages, tools=tool_schemas, temperature=0)
msg = resp.choices[0].message
print("TOOL CALLS:", msg.tool_calls)

messages.append({
    "role": "assistant",
    "content": msg.content or "",
    "tool_calls": [{"id": tc.id, "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                   for tc in (msg.tool_calls or [])],
})

for tc in msg.tool_calls or []:
    args = json.loads(tc.function.arguments)
    result = TOOLS[tc.function.name](**args)
    print("RESULT:", result)
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})

resp = completion(model=MODEL, messages=messages, tools=tool_schemas, temperature=0)
print("ANSWER:", resp.choices[0].message.content)