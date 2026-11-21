# Lab 2: Architectures: A ReAct Agent From Scratch: Concept Check

Answer in your own words before the Wednesday session (independent work). Your answers feed Section 2 of your lab report (Concept and classical root).

## Q1. Classify a thermostat, a chess engine and a ReAct agent as reactive, deliberative or hybrid, with one reason each.

_Your answer:_ 1. **Thermostat: reactive.** It follows one rule (too cold, so heat on), with no plan or memory.
   **Chess engine: deliberative.** It searches future moves and plans before acting.
   **ReAct agent: hybrid.** Thoughts plan across steps (deliberative), and each step reacts to the latest Observation (reactive).


## Q2. In the trace above, which lines are percepts, and which are actions?

_Your answer:_**Percepts:** the user question and every `Observation:` line (1025, 175).
   **Actions:** every `Action:` / `Action Input:` pair (calculator calls and finish).


## Q3. Why do we pass `stop=["Observation:"]` when calling the model?

_Your answer:_`stop=["Observation:"]` stops the model before it writes its own Observation.
   Without it, the model can invent tool results. trace_4_bug.txt shows this:
   it made up a Wikipedia summary that does not exist.


## Q4. Map the trace above to the BDI terms belief, desire and intention.

_Your answer:_ **Belief:** the conversation so far, including Observations (e.g. total cost is 1025).
   **Desire:** answer the user's question (money left).
   **Intention:** the committed plan in the Thought (add the costs, then subtract from 1200).

