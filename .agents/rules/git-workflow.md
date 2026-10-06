## Git Workflow & Issue-Driven Development Rule

Strict workflow for all code changes and contributions:

1. **NO Direct Pushing to Base Branch (`main` / `master`):**
   - Direct commits and direct pushes to `main` or `master` are strictly forbidden under all circumstances.

2. **Issue-First Requirement (Detailed User Story):**
   - Before writing or pushing code for a feature, enhancement, or fix, create a detailed GitHub Issue using the GitHub CLI (`gh issue create`).
   - The issue must contain:
     - **User Story:** Formatted as `As a <user/developer>, I want <capability>, so that <benefit>`.
     - **Context & Motivation:** Comprehensive explanation of why this change is needed.
     - **Technical Specification:** Architecture, files affected, API endpoints, schema changes, and UI/UX design considerations.
     - **Acceptance Criteria:** A strict checklist of verifiable requirements.

3. **Feature Branch Workflow:**
   - Always branch off the latest base branch into a descriptive branch name:
     - `feat/<feature-name>`
     - `fix/<bug-name>`
     - `refactor/<scope-name>`
   - Implement, test, and verify on this branch.

4. **Quality Gates Before PR:**
   - Run `pytest` to ensure all tests pass (0 failures).
   - Run `npm run build` in `frontend/` to verify zero build or packaging errors.
   - Run `python -m graphify update .` to sync the AST knowledge graph.

5. **Pull Request (PR) Workflow:**
   - Push the feature branch to remote (`git push -u origin <branch-name>`).
   - Create a Pull Request via GitHub CLI (`gh pr create`) with a detailed description and link to close the issue (`Closes #<issue-number>`).
   - Merge the PR via GitHub CLI (`gh pr merge --squash` or `--merge`) only after verification.
