# Lab 2 Baseline: model with no tools

Model: groq/openai/gpt-oss-20b

## Budget question (correct answer: GHS 175)
| Run | Answer | Correct? |
|-----|--------|----------|
| 1 | GHS 175 | Correct |
| 2 | GHS 175 | Correct |
| 3 | GHS 175 | Correct |

## Factual questions
| Question | Answer | Correct? | Confidence |
|----------|--------|----------|------------|
| Capital of Bono East Region | Techiman | Correct | High |
| Who founded Makola Market | "Kofi Yeboah", early 19th century | Unsupported: likely hallucinated | High |

## Observation
Arithmetic was correct in all 3 runs, but the model calculates in text, so
nothing guarantees accuracy. On Makola it named a founder with no source.
An earlier run of the same question said there was "no single founder",
so the model contradicts itself and sounds confident both times. Tools fix
this: a calculator for exact maths and Wikipedia for checkable facts.