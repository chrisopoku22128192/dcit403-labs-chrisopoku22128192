import os
import sys
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
MODEL = os.getenv("LLM_MODEL")
TEMP = float(sys.argv[1]) if len(sys.argv) > 1 else 0

resp = completion(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "In one sentence, what is an intelligent agent?"},
    ],
    temperature=TEMP,
)

print(f"[temperature={TEMP}]")
print(resp.choices[0].message.content)
print(resp.usage)