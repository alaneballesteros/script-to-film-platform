# Contributing to Script to Film Platform

Welcome! This guide will help you collaborate effectively on this project using GitHub Flow.

## Table of Contents

- [Getting Started](#getting-started)
- [GitHub Flow Overview](#github-flow-overview)
- [Development Workflow](#development-workflow)
- [Branch Naming Convention](#branch-naming-convention)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Review Guidelines](#code-review-guidelines)
- [Resolving Conflicts](#resolving-conflicts)

## Getting Started

### First Time Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/script-to-film-platform.git
   cd script-to-film-platform
   ```

2. **Set up your git identity (if not already done):**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

3. **Set up the development environment:**

   **Backend:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

   **Frontend:**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application locally:**

   Terminal 1 (Backend):
   ```bash
   source venv/bin/activate
   python -m uvicorn script_to_film.main:app --reload --port 8000
   ```

   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```

## GitHub Flow Overview

We use **GitHub Flow** - a simple, branch-based workflow perfect for small teams.

### The Basic Cycle

```
main branch (always deployable)
     ↓
  Create feature branch
     ↓
  Make changes & commit
     ↓
  Push to GitHub
     ↓
  Open Pull Request
     ↓
  Code Review & Discussion
     ↓
  Merge to main
     ↓
  Delete feature branch
```

### Key Principles

1. **`main` branch is always deployable** - never commit broken code to main
2. **Create descriptive branches** - one branch per feature/fix
3. **Commit often** - small, logical commits are better than large ones
4. **Open Pull Requests early** - even for work in progress (use "Draft PR")
5. **Review thoroughly** - all code must be reviewed before merging
6. **Keep branches short-lived** - merge within 1-3 days when possible

## Development Workflow

### Starting New Work

```bash
# 1. Make sure you're on main and it's up to date
git checkout main
git pull origin main

# 2. Create a new branch for your feature
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... edit files ...

# 4. Check what changed
git status
git diff

# 5. Stage and commit your changes
git add .
git commit -m "Add detailed description of your changes"

# 6. Push your branch to GitHub
git push origin feature/your-feature-name

# 7. Go to GitHub and create a Pull Request
```

### Continuing Work on an Existing Branch

```bash
# 1. Switch to your branch
git checkout feature/your-feature-name

# 2. Get latest changes from main (important!)
git pull origin main

# 3. Make your changes and commit
git add .
git commit -m "Your commit message"

# 4. Push to update your PR
git push origin feature/your-feature-name
```

### Keeping Your Branch Updated

```bash
# While on your feature branch
git checkout feature/your-feature-name

# Pull latest changes from main
git pull origin main

# If there are conflicts, resolve them, then:
git add .
git commit -m "Merge main into feature/your-feature-name"
git push origin feature/your-feature-name
```

## Branch Naming Convention

Use these prefixes to make branch purposes clear:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features | `feature/user-authentication` |
| `fix/` | Bug fixes | `fix/video-generation-error` |
| `refactor/` | Code improvements (no new features) | `refactor/api-error-handling` |
| `docs/` | Documentation updates | `docs/api-endpoints` |
| `test/` | Adding or updating tests | `test/script-parser-unit-tests` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

**Examples:**
```bash
git checkout -b feature/ai-script-generation
git checkout -b fix/frontend-routing-bug
git checkout -b refactor/cleanup-video-service
git checkout -b docs/setup-instructions
```

## Commit Message Guidelines

### Format

```
<type>: <short summary in present tense>

<optional detailed description>

<optional footer>
```

### Types

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Examples

**Good commits:**
```bash
git commit -m "feat: Add OpenAI integration for script generation"
git commit -m "fix: Resolve CORS error in frontend API calls"
git commit -m "docs: Update README with new API endpoints"
git commit -m "refactor: Extract scene parsing logic into separate service"
```

**Bad commits:**
```bash
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "asdf"
git commit -m "final version"
```

### Detailed Commit Example

```bash
git commit -m "feat: Add user authentication with JWT

- Implement JWT token generation and validation
- Add login and register endpoints
- Create authentication middleware
- Update API documentation

Closes #12
```

## Pull Request Process

### 1. Creating a Pull Request

After pushing your branch to GitHub:

1. Go to the repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Fill out the PR template (see below)
5. Assign a reviewer (your teammate)
6. Click "Create pull request"

### 2. PR Title Format

```
<type>: <clear description>
```

Examples:
- `feat: Add video prompt generation endpoint`
- `fix: Resolve database connection timeout`
- `docs: Update contributing guidelines`

### 3. PR Description Template

Use this format (we'll set this up automatically):

```markdown
## Description
Brief summary of what this PR does and why.

## Changes Made
- List of specific changes
- Another change
- More changes

## Testing Done
- [ ] Tested locally (backend + frontend)
- [ ] All existing tests pass
- [ ] Added new tests if needed

## Screenshots (if UI changes)
[Add screenshots here]

## Related Issues
Closes #issue_number (if applicable)
```

### 4. Review Process

**As the Author:**
- Respond to all review comments
- Make requested changes
- Re-request review after updates
- Be open to feedback

**As the Reviewer:**
- Review within 24 hours when possible
- Be constructive and kind
- Test the changes locally if needed
- Approve when satisfied

### 5. Merging

Once approved:
1. Make sure your branch is up to date with main
2. Click "Merge pull request"
3. Choose "Squash and merge" for cleaner history (recommended)
4. Delete the branch after merging

## Code Review Guidelines

### What to Look For

**Functionality:**
- Does the code do what it's supposed to?
- Are there any bugs or edge cases not handled?

**Code Quality:**
- Is the code readable and well-organized?
- Are there any code smells or anti-patterns?
- Is error handling adequate?

**Testing:**
- Are there tests for new functionality?
- Do all tests pass?

**Documentation:**
- Are complex parts commented?
- Is the API documented?
- Are README/docs updated if needed?

**Style:**
- Does it follow project conventions?
- Is formatting consistent?

### Review Comments Examples

**Good feedback:**
```
Consider extracting this logic into a separate function for better testability.
```

```
This could potentially cause a memory leak. Have you considered using a
cleanup function in the useEffect hook?
```

```
Great solution! Just a minor suggestion: we could use the existing
helper function from utils/validation.py here.
```

**Less helpful feedback:**
```
This is wrong.
```

```
Why did you do it this way?
```

## Resolving Conflicts

### When Conflicts Happen

Conflicts occur when:
- You and your teammate edit the same file
- Main branch has changes that conflict with yours

### Resolving Conflicts

```bash
# 1. Update your branch with latest main
git checkout feature/your-branch
git pull origin main

# 2. Git will show conflicts like:
#    CONFLICT (content): Merge conflict in src/file.py

# 3. Open the conflicted file and look for:
<<<<<<< HEAD
Your changes
=======
Changes from main
>>>>>>> main

# 4. Edit the file to resolve conflicts (keep what you need)

# 5. Mark as resolved and commit
git add .
git commit -m "Merge main and resolve conflicts"
git push origin feature/your-branch
```

### Avoiding Conflicts

1. **Pull from main frequently:**
   ```bash
   git pull origin main
   ```

2. **Communicate what you're working on**

3. **Keep PRs small and merge quickly**

4. **Divide work by files/components when possible:**
   - Person A: Backend API development
   - Person B: Frontend UI components

## Quick Reference

### Daily Workflow Cheat Sheet

```bash
# Starting the day
git checkout main
git pull origin main
git checkout -b feature/my-new-feature

# During work
git add .
git commit -m "feat: your change description"
git push origin feature/my-new-feature

# Before ending the day
git push origin feature/my-new-feature  # Backup your work

# Switching tasks
git add .
git commit -m "WIP: save current progress"
git checkout other-branch
```

### Common Commands

```bash
# See all branches
git branch -a

# Delete local branch
git branch -d branch-name

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# See commit history
git log --oneline

# Check what branch you're on
git branch

# Update main
git checkout main
git pull origin main
```

## Getting Help

- Check this guide first
- Ask your teammate
- Search GitHub Issues
- Check Git documentation: https://git-scm.com/doc

## Additional Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

Happy coding!
