# Step 2: First LLM call

Model: groq/openai/gpt-oss-120b

Three parts of the call: model (LLM_MODEL), messages (system + user), settings (temperature).

| Temp | Runs | Result |
|------|------|--------|
| 0 | 3 | Identical answers, identical tokens (164) |
| 1 | 3 | Different wording each run ("entity", "effectors"; one run dropped "sensors") |

Tokens: prompt = 90 (constant), completion = 71 to 78, of which 28 to 38 were
hidden reasoning tokens.

Note: temperature 0 was consistent here, but this is not guaranteed.