# GitHub Team Workflow Manager

> A step-by-step GitHub integration pipeline specification to ensure secure version control and code integration in a team collaboration environment.

---

## 1. Definition & Role
- **Version Control Standardization:** Prevents conflicts that may occur during feature branching, code commits, and remote repository synchronization/merging, ensuring adherence to the team's configuration management rules.
- **Error Prevention:** Protects the integrity of the remote repository through safety mechanisms such as blocking force pushes and preventing the exposure of sensitive information.
- **Workflow Pipeline Control:** Prevents indiscriminate overwriting by single commands and controls AI actions by breaking them down into validation, branching, committing, and sharing phases.

## 2. Execution Pipeline

### Phase 1: Status Check & Safe Pull
1. **Check Working Directory:** Verify if there are any local changes using `git status`. If there are uncommitted changes, temporarily stash them using `git stash`.
2. **Remote Synchronization:** Execute `git fetch` and `git pull --rebase origin [branch]` to update the local repository with the latest remote code without creating a merge commit.
3. **Restore State:** If necessary, restore the previous work using `git stash pop` and check for any merge conflicts.

### Phase 2: Branching Strategy
1. **Create Branch:** When adding a new feature or fixing a bug, do not work directly on the `main` branch. Create a new branch adhering to naming conventions (e.g., `feat/`, `fix/`, `chore/`) using `git checkout -b [branch_name]`.
2. **Isolate Work:** All modifications MUST be performed within the isolated branch.

### Phase 3: Atomic Commit
1. **Isolate Changes:** Avoid using `git add .`. Selectively stage only the files related to a logical unit of work (`git add [file_path]`).
2. **Standardized Commit Messages:** Write commit messages following the Conventional Commits specification (e.g., `feat: [feature summary]`) to leave a clear work history.

### Phase 4: Push & PR (Pull Request)
1. **Remote Push:** Upload the working branch to the remote repository using `git push origin [branch_name]`.
2. **Create PR:** Utilize GitHub tools to create a PR requesting a review from team members, detailing the purpose and impact of the changes.

## 3. Constraints
1. **Prohibition of Force Push:** Under no circumstances should force overwrite commands like `git push --force` be used on shared branches such as `main` or `master`.
2. **Verification of Hardcoded Sensitive Information:** Before committing, unconditionally verify that there are no security threat elements included, such as API Keys, passwords, or local system absolute paths.
3. **Maintain Independent Processes:** Each Phase is executed independently, and Git commands for the next phase are only executed after the integrity of the previous phase (e.g., no merge conflicts) has been secured.
