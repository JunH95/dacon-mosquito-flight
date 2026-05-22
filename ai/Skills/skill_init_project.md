# Project Initialization Pipeline

> A scaffolding skill that sets up a new local project environment by migrating necessary global Agents and Skills into a `.ai` directory. Supports 'Zero-State Scaffold' to allow local PM meetings before domain decisions are made.

---

## 1. Definition & Role
- **Zero-State Bootstrapper:** Unconditionally injects core Agents (PM, Lead, QA) and Skills into an empty project so the user can begin localized planning without needing prior domain confirmation.
- **Context Isolator:** Prevents global context contamination by physically segregating the scoped Agents, Skills, and local Rules into the target project's `.ai` subdirectory.

## 2. Execution Pipeline
1. **Parameter Gathering:** 
   - Ask the user for the absolute path of the new target project.
   - *Domain is Optional:* If the user hasn't held a PM meeting yet, proceed with 'Zero-State Scaffold'.
2. **Directory Scaffolding:** Execute shell commands to create the structure inside the target project:
   - `<target_project>\.ai\Agents`
   - `<target_project>\.ai\Skills`
   - `<target_project>\.ai\Rules`
3. **Phase 1: Core Migration (Zero-State Scaffold):** Execute shell commands (`Copy-Item`) to unconditionally copy baseline assets so local meetings can occur:
   - Global Core Agents: `c:\dev\ai_workspace\Agents\*` -> `.ai\Agents`
   - Global Core Skills: `c:\dev\ai_workspace\Skills\*` -> `.ai\Skills`
4. **Phase 2: Domain Rule Fetching (Deferred/Optional):** 
   - If a Target Domain is known: copy `c:\dev\ai_workspace\Rules\Domains\<TargetDomain>\*` -> `.ai\Rules`
   - If unknown: Skip this step. The user can fetch rules later after holding a local PM meeting.
5. **Verification:** Verify that the files were successfully copied and notify the user they can now `@mention` PM/Lead locally.

## 3. Constraints
- **System Isolation:** NEVER copy the `System\` directory. Those are meta-tools strictly reserved for the `ai_workspace` master repository.
- **Global Rule Exclusion:** Do NOT copy `rule_global.md` as it is natively injected via IDE Customizations.
- **Non-Destructive:** NEVER overwrite existing `.ai` directories in the target project without explicit user confirmation.
- **Absolute Paths Required:** Always use absolute file paths in shell commands to prevent accidental copying to incorrect relative directories.
