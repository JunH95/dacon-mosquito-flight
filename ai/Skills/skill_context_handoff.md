# Context Handoff Workflow

> A state serialization pipeline that extracts the current chat session's progress, unresolved issues, and next objectives into a physical markdown file (`handoff_state.md`) to seamlessly transfer context to a new chat session.

---

## 1. Definition & Role
- **Context Preserver:** Prevents Context Degradation (hallucination, slow responses) by migrating volatile chat memory into a permanent file-based state.
- **Session Bridge:** Acts as an official handover document between an old, bloated chat session and a fresh, high-performance new chat session.

## 2. Execution Pipeline
1. **State Abstraction:** Analyze the entire current conversation history and summarize the "Completed Tasks".
2. **Issue Logging:** Identify any currently pending bugs, unresolved errors, or blocked states.
3. **Next Objectives:** Define exactly what the new AI session should do immediately upon reading the handoff file.
4. **File Generation:** Write these findings into a file named `[project_name]_handoff_state.md` (e.g., `ai_workspace_handoff_state.md`) at the **root directory of the current project**. Ensure the file includes clear instructions for the AI in the new chat.
5. **Session Termination Prompt:** After generating the file, instruct the user: "Handoff complete. Please open a New Chat and mention `@[project_name]_handoff_state.md`."

## 3. Constraints
- **Absolute Conciseness:** The generated `handoff_state.md` MUST be extremely concise (bullet points only) to minimize the token footprint in the new chat's context window.
- **Reference Over Inclusion:** Do NOT include full source code in the handoff file. Reference absolute file paths (e.g., `Check src/main.py`) instead.
- **No Implementation:** Do not attempt to fix bugs or write code during the handoff process. The sole purpose is to document the state.
