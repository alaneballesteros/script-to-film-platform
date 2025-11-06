# GitHub Flow - Step-by-Step Guide

This guide provides a practical, step-by-step walkthrough of GitHub Flow for the Script to Film Platform project.

## What is GitHub Flow?

GitHub Flow is a lightweight, branch-based workflow that supports teams practicing continuous deployment.

**Core Idea:** Anything in the `main` branch is always deployable.

## Visual Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        GITHUB FLOW                           │
└─────────────────────────────────────────────────────────────┘

    main branch (always stable)
    │
    ├─── Create feature branch
    │    │
    │    ├─── Make commits
    │    │
    │    └─── Open Pull Request
    │         │
    │         ├─── Discuss & Review
    │         │
    │         ├─── Make more commits (if needed)
    │         │
    │         └─── Merge to main
    │              │
    └──────────────┘
    │
    (Repeat)
```

## The Complete Workflow

### Step 1: Create a Repository on GitHub

1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon → "New repository"
3. Name it: `script-to-film-platform`
4. Choose: Public or Private
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

GitHub will show you setup instructions. Keep this page open!

### Step 2: Connect Your Local Repo to GitHub

```bash
# In your project directory
cd /Users/alanballesterossandoval/script-to-film-platform

# Add GitHub as the remote
git remote add origin https://github.com/YOUR_USERNAME/script-to-film-platform.git

# Verify it worked
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/script-to-film-platform.git (fetch)
origin  https://github.com/YOUR_USERNAME/script-to-film-platform.git (push)
```

### Step 3: Push Your Initial Commit

```bash
# Create initial commit (if not already done)
git add .
git commit -m "Initial commit: Project setup with backend and frontend"

# Push to GitHub
git branch -M main  # Rename branch to 'main' if needed
git push -u origin main
```

Now your code is on GitHub!

### Step 4: Invite Your Collaborator

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Click "Collaborators" in the left sidebar
4. Click "Add people"
5. Enter your friend's GitHub username or email
6. Click "Add [username] to this repository"

Your friend will receive an email invitation.

### Step 5: Collaborator Clones the Repo

Your friend should:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/script-to-film-platform.git
cd script-to-film-platform

# Set up the project (follow CONTRIBUTING.md)
# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Frontend
cd frontend
npm install
```

---

## Daily Development Workflow

### Scenario 1: You Want to Add a New Feature

**Let's say you want to add "User Authentication"**

#### 1. Start from Main

```bash
# Make sure you're on main
git checkout main

# Get the latest code
git pull origin main
```

#### 2. Create a Feature Branch

```bash
# Create and switch to new branch
git checkout -b feature/user-authentication

# Verify you're on the new branch
git branch
# Should show: * feature/user-authentication
```

#### 3. Make Your Changes

```bash
# Make your code changes in your editor
# For example, create auth files, add routes, etc.
```

#### 4. Check What Changed

```bash
# See what files changed
git status

# See the actual changes
git diff
```

#### 5. Commit Your Changes

```bash
# Stage all changes
git add .

# Or stage specific files
git add src/script_to_film/api/auth.py
git add src/script_to_film/models/user.py

# Commit with a descriptive message
git commit -m "feat: Add user authentication with JWT tokens

- Create User model with password hashing
- Add login and register endpoints
- Implement JWT token generation
- Add authentication middleware"
```

#### 6. Push to GitHub

```bash
# Push your branch to GitHub
git push origin feature/user-authentication
```

#### 7. Create a Pull Request

1. Go to your repository on GitHub
2. You'll see a yellow banner saying "Compare & pull request" - click it
3. Fill out the PR template:
   - **Title:** `feat: Add user authentication`
   - **Description:** Explain what you did and why
4. Assign your teammate as a reviewer
5. Click "Create pull request"

#### 8. Wait for Review

Your teammate will:
- Review your code
- Leave comments if they have questions
- Approve if everything looks good

#### 9. Address Feedback (if any)

If your teammate requests changes:

```bash
# Make the requested changes
# ... edit files ...

# Commit the changes
git add .
git commit -m "Address PR feedback: Add password validation"

# Push to update the PR
git push origin feature/user-authentication
```

The PR will automatically update!

#### 10. Merge the PR

Once approved:

1. Go to the PR on GitHub
2. Click "Merge pull request"
3. Click "Confirm merge"
4. Click "Delete branch" (to keep things clean)

#### 11. Update Your Local Main

```bash
# Switch back to main
git checkout main

# Pull the merged changes
git pull origin main

# Delete your local feature branch (optional but recommended)
git branch -d feature/user-authentication
```

Done! Your feature is now in main.

---

### Scenario 2: Your Teammate Adds a Feature While You're Working

**You're working on `feature/video-export` and your friend merges `feature/user-auth` to main.**

#### Keep Your Branch Updated

```bash
# While on your feature branch
git checkout feature/video-export

# Pull the latest changes from main
git pull origin main
```

This brings your teammate's changes into your branch, reducing conflicts later.

#### If There Are Conflicts

Git will tell you which files have conflicts:

```
CONFLICT (content): Merge conflict in src/script_to_film/api/routes.py
```

Open the file and look for:

```python
<<<<<<< HEAD
# Your changes
def export_video():
    pass
=======
# Changes from main (your teammate's code)
def authenticate_user():
    pass
>>>>>>> main
```

**Fix it by keeping both** (or whatever makes sense):

```python
def authenticate_user():
    pass

def export_video():
    pass
```

Then:

```bash
# Mark conflicts as resolved
git add src/script_to_film/api/routes.py

# Complete the merge
git commit -m "Merge main into feature/video-export"

# Push the updated branch
git push origin feature/video-export
```

---

## Common Scenarios & Solutions

### Scenario: You Made Changes on Main by Mistake

```bash
# DON'T PANIC!

# Create a new branch with your changes
git checkout -b feature/accidental-work

# Push it
git push origin feature/accidental-work

# Go back to main
git checkout main

# Reset main to match GitHub
git fetch origin
git reset --hard origin/main
```

Now create a PR from your new branch!

### Scenario: You Want to Work on Two Things at Once

```bash
# Work on feature 1
git checkout -b feature/thing-one
# ... make changes ...
git add .
git commit -m "Work on thing one"
git push origin feature/thing-one

# Switch to feature 2 (your changes to thing-one are safe!)
git checkout main
git checkout -b feature/thing-two
# ... make changes ...
git add .
git commit -m "Work on thing two"
git push origin feature/thing-two

# Switch between them anytime
git checkout feature/thing-one
git checkout feature/thing-two
```

### Scenario: You Need to Test Your Teammate's PR

```bash
# Fetch all branches from GitHub
git fetch origin

# Check out their branch
git checkout feature/their-feature-name

# Run the app locally to test
# Backend
source venv/bin/activate
python -m uvicorn script_to_film.main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev

# When done testing, go back to your branch
git checkout feature/your-feature
```

### Scenario: You Want to Undo Your Last Commit

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Now you can modify and commit again
```

---

## Branch Protection & Settings (Recommended)

Once your repo is on GitHub, set up protection:

### 1. Protect Main Branch

1. Go to repository Settings
2. Click "Branches"
3. Click "Add rule"
4. Branch name pattern: `main`
5. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Require status checks to pass (if you set up CI later)
6. Click "Create"

This prevents direct pushes to main - everything must go through PR!

### 2. Auto-Delete Branches

1. Go to repository Settings
2. Scroll to "Pull Requests"
3. Enable: ✅ Automatically delete head branches

This keeps your repo clean after merging PRs.

---

## Division of Work Strategy

To minimize conflicts, consider dividing work by area:

### Option 1: By Component

**Person A (Backend Focus):**
- `src/script_to_film/api/` - API routes
- `src/script_to_film/services/` - Business logic
- `src/script_to_film/models/` - Data models

**Person B (Frontend Focus):**
- `frontend/src/components/` - UI components
- `frontend/src/services/` - API integration
- `frontend/src/styles/` - Styling

**Shared (Coordinate):**
- API contracts (discuss endpoint changes together)
- Database schema changes
- Documentation

### Option 2: By Feature

**Person A:**
- User authentication (backend + frontend)
- User profile management

**Person B:**
- Script generation (backend + frontend)
- Video export functionality

---

## Best Practices Summary

### DO:
- ✅ Pull from main frequently
- ✅ Commit often with clear messages
- ✅ Keep PRs small and focused
- ✅ Review code within 24 hours
- ✅ Communicate what you're working on
- ✅ Test locally before pushing
- ✅ Write meaningful PR descriptions

### DON'T:
- ❌ Commit directly to main
- ❌ Leave PRs open for days
- ❌ Commit broken code
- ❌ Commit `.env` files or secrets
- ❌ Force push (`git push -f`) without discussing
- ❌ Ignore merge conflicts
- ❌ Skip code reviews

---

## Quick Command Reference

```bash
# Daily commands
git status                          # Check current state
git pull origin main               # Update main branch
git checkout -b feature/name       # Create new branch
git add .                          # Stage all changes
git commit -m "message"            # Commit changes
git push origin branch-name        # Push to GitHub

# Branch management
git branch                         # List local branches
git branch -a                      # List all branches (including remote)
git branch -d branch-name          # Delete local branch
git checkout branch-name           # Switch branches

# Syncing
git fetch origin                   # Get latest from GitHub (no merge)
git pull origin main               # Get and merge latest from main
git pull origin branch-name        # Update current branch from GitHub

# Viewing history
git log                            # View commit history
git log --oneline                  # Compact commit history
git diff                           # See unstaged changes
git diff --staged                  # See staged changes

# Undoing
git reset --soft HEAD~1            # Undo last commit, keep changes
git reset --hard HEAD              # Discard all local changes
git checkout -- file.py            # Discard changes to specific file
```

---

## Troubleshooting

### "fatal: remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/script-to-film-platform.git
```

### "Permission denied (publickey)"

You need to set up SSH keys or use HTTPS:

```bash
# Use HTTPS instead
git remote set-url origin https://github.com/YOUR_USERNAME/script-to-film-platform.git
```

### "Your branch is behind 'origin/main'"

```bash
git pull origin main
```

### "refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

---

## Next Steps

1. **Create GitHub repository** (see Step 1)
2. **Push your code** (see Step 3)
3. **Invite collaborator** (see Step 4)
4. **Set up branch protection** (see Branch Protection section)
5. **Start building!** (use Scenario 1 as template)

---

## Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Learning Lab](https://lab.github.com/)
- Our [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines

Happy collaborating!
