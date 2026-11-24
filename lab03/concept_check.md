# Lab 3: Percepts and Actions as Tools: Function Calling and MCP: Concept Check

Answer in your own words before the Wednesday session (independent work). Your answers feed Section 2 of your lab report (Concept and classical root).

## Q1. List one advantage and one disadvantage of native function calling compared with the Lab 2 text protocol.

_Your answer:_ **Advantage:** the API enforces the tool-call format, so there is no regex and no parsing
   failures (Lab 2 needed first_step(), FORMAT_HELP and recover_tool_call()).
   **Disadvantage:** the reasoning is hidden; there are no visible Thought lines, so it is harder
   to see why the model chose a tool. It also depends on the model supporting function calling.


## Q2. In MCP, what is the difference between a tool and a resource? Give a pharmacy example of each.

_Your answer:_A **tool** is a function the model can call, which may change things:
   `record_sale` reduces stock. A **resource** is read-only data the app can load into context:
   the stock list or a price list exposed as a resource.


## Q3. Why should `record_sale` check the quantity even though the system prompt already says "never oversell"?

_Your answer:_The prompt rule is only a request the model can ignore; code in the tool always runs.
   In my test, calling `record_sale("amoxicillin", "500mg", 500)` directly was refused by the
   tool itself ("only 38 packs in stock"), with no model involved.


## Q4. Which messages in the worked example are percepts?

_Your answer:_ Message 3, the **tool** message holding the stock row, is the percept. Message 1, the user's
   question, is also a percept. Message 2 is the agent's action and message 4 is its reply.

