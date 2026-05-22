# GitHub Solo Workflow Manager

> A lightweight pipeline for single-developer environments that skips branching and PR procedures to ensure rapid deployment and secure main branch version control.

---

## 1. Definition & Role
- **Maximize Development Productivity:** Bypasses complex collaborative branching and Pull Request (PR) processes to quickly deploy and update the repository.
- **Minimal Automated Verification:** Controls state verification and local-remote synchronization pipelines optimized for a single-developer environment to prevent commit history entanglement.
- **Secure Remote Repository Integrity:** Systematically blocks remote history corruption or sensitive information exposure that can occur even when pushing directly to the main branch.

## 2. Execution Pipeline

### Phase 1: Safe Pull & Sync
1. **Check Local State:** Execute `git status` to diagnose any unstaged changes.
2. **Apply Latest Remote Changes:** Before starting local work, or immediately before a remote push, execute `git pull origin main` to safely merge the latest codebase from the remote repository to the local environment.
3. **Resolve Conflicts:** If conflicts occur with the remote code, manually resolve them before proceeding to the next phase.

### Phase 2: Atomic Commit to Main
1. **Analyze and Stage Changes:** Instead of bulk adding with `git add .`, select and stage files associated with a specific feature unit (`git add [file_path]`).
2. **Adhere to Commit Message Standards:** Use Conventional Commits specifications to clearly state the intent of the change (e.g., `feat: add database schema`).

### Phase 3: Direct Push
1. **Final Static Analysis:** Re-verify that there are no hardcoded passwords, private keys, or unnecessary test codes within the code.
2. **Immediate Deployment:** Upon successful verification, directly push to the remote `main` branch to update the version (`git push origin main`).

## 3. Constraints
1. **Permanent Ban on Overwriting Remote History:** Even in a solo development environment, to preserve history and ensure recovery safety, `git push --force` related commands MUST NOT be used under any circumstances.
2. **Prevent Hardcoded Sensitive Information Leaks:** A static text search MUST be unconditionally performed to ensure no information that could become a vulnerability upon external exposure (such as API Keys or local absolute paths) has leaked into the target files for commit and push.
3. **Pre-synchronization Prerequisite:** To completely prevent remote rejection errors (non-fast-forward) caused by attempting a push without executing `git pull` first, the push command MUST only be assembled when Phase 1 has been completed.
