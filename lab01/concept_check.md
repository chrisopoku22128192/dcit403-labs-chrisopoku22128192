# Lab 1: Agents Then and Now: PEAS and Your First LLM Call: Concept Check

Answer in your own words before the Wednesday session (independent work). Your answers feed Section 2 of your lab report (Concept and classical root).

## Q1. Give the PEAS description of a self-checkout machine at a supermarket.

_Your answer:_**PEAS: self-checkout machine**
   - Performance: correct total, accurate scanning, fast checkout, prevents theft
   - Environment: shoppers, products with barcodes, payment cards and MoMo, store staff
   - Actuators: screen display, beeps, receipt printer, bagging-area alerts, calling staff
   - Sensors: barcode scanner, weighing scale, touchscreen, card reader


## Q2. Is the Campus Info Bot's environment episodic or sequential? Justify your answer using what the bot needs to remember.

_Your answer:_**Sequential.** The bot must remember earlier turns. In my test, "What time does it close?" only
   made sense because the bot remembered that "it" was the Department Office from the previous turn.


## Q3. Which part of an LLM agent plays the role of the percept sequence?

_Your answer:_The **messages list (`history`)** sent to the model every turn. It holds everything the agent
   has perceived so far.


## Q4. An agent gives a wrong office location because its facts block was out of date. Was it irrational? Explain.

_Your answer:_**No, it was not irrational.** A rational agent picks the best action given what it knows. It
   answered correctly from its facts block, but the facts were out of date. The fault is in its
   knowledge, not its reasoning.

