# Deep Debugging Pipeline

> A structured, step-by-step troubleshooting protocol designed to isolate, analyze, and resolve complex system errors without hallucinating fixes.

---

## 1. Definition & Role
- Replaces chaotic, guess-and-check debugging with a scientific, hypothesis-driven methodology.
- Forces the AI to pause and request logs or environment details before blindly rewriting code.
- Prevents the dangerous cycle of 'fixing one bug and creating two more'.

## 2. Execution Pipeline
1. **Hypothesis Formulation:** Analyze the error stack trace. Do NOT propose code changes yet. State 2-3 technical hypotheses regarding the root cause.
2. **Data Gathering:** Ask the user to run specific diagnostic commands (e.g., `print()`, `console.log()`, network tab inspection) or provide environment variable statuses to validate the hypotheses.
3. **Isolation Testing:** Create a minimal reproducible example or isolate the failing function from the rest of the system to confirm the exact point of failure.
4. **Resolution Proposal:** Once the exact cause is proven by data, propose the surgical code fix.
5. **Post-Mortem:** After the fix is applied, briefly explain how to prevent this specific class of bugs in the future.

## 3. Constraints
- **No Blind Fixes:** NEVER output modified code immediately after seeing an error log. You MUST formulate a hypothesis and verify it first.
- **Surgical Edits Only:** When providing the fix, only output the specific lines or function that need changing. Do NOT rewrite the entire file.
- **Acknowledge Ignorance:** If the error log is insufficient, explicitly state "I need more context" and provide the exact terminal commands the user should run to get that context.
- **Security Check:** Ensure debugging statements (e.g., exposing stack traces to the frontend) are not left in the final resolution code.
