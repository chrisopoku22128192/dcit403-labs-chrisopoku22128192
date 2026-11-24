import os
import sys
import json
import asyncio
from dotenv import load_dotenv
from litellm import acompletion
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "groq/openai/gpt-oss-120b")
HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = StdioServerParameters(command=sys.executable, args=[os.path.join(HERE, "server.py")])

SYSTEM_PROMPT = ("You are a pharmacy stock assistant. Use the tools to answer. "
                 "Answer only from tool results; never invent stock, prices or dates. "
                 "Keep answers short.")


def tool_result_text(result):
    if getattr(result, "structuredContent", None):
        return json.dumps(result.structuredContent)
    return "\n".join(getattr(c, "text", "") for c in result.content)


async def run_agent(session, schemas, question, max_steps=6):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    for _ in range(max_steps):
        resp = await acompletion(model=MODEL, messages=messages, tools=schemas, temperature=0)
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [{"id": tc.id, "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                           for tc in msg.tool_calls],
        })
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            print(f"  -> {tc.function.name}({args})")
            result = await session.call_tool(tc.function.name, args)
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": tool_result_text(result)})
    return "Stopped: reached max_steps without a final answer."


async def main(questions):
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            print("Discovered tools:", [t.name for t in tools])
            schemas = [{"type": "function", "function": {
                "name": t.name, "description": t.description,
                "parameters": t.inputSchema}} for t in tools]
            for q in questions:
                print(f"\nQ: {q}")
                answer = await run_agent(session, schemas, q)
                print(f"A: {answer}")


if __name__ == "__main__":
    qs = sys.argv[1:] or ["Do we have amoxicillin 500mg?"]
    asyncio.run(main(qs))