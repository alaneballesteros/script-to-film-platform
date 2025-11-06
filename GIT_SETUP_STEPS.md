# Git Setup & GitHub Collaboration - Next Steps

Your repository has been initialized and all collaboration files are ready! Follow these steps to push to GitHub and start collaborating.

## Step 1: Configure Git (One-time setup)

You need to tell git who you are:

```bash
# Set your name (use your real name or GitHub username)
git config --global user.name "Your Name"

# Set your email (use the email associated with your GitHub account)
git config --global user.email "your.email@example.com"

# Verify it worked
git config --global user.name
git config --global user.email
```

**Important:** Use the same email as your GitHub account!

## Step 2: Create Initial Commit

Now commit all your code:

```bash
# Make sure you're in the project directory
cd /Users/alanballesterossandoval/script-to-film-platform

# Stage all files
git add .

# Create the initial commit
git commit -m "Initial commit: Script to Film Platform

- Backend API with FastAPI
- React frontend with Vite
- AI service integration (OpenAI, Anthropic)
- Video generation capabilities
- Complete documentation and collaboration guides"

# Verify the commit was created
git log
```

## Step 3: Create GitHub Repository

### Option A: Using GitHub Website (Easier)

1. Go to https://github.com
2. Click the "+" icon in top right → "New repository"
3. Fill in:
   - **Repository name:** `script-to-film-platform`
   - **Description:** "AI-powered platform for converting scripts to short films"
   - **Visibility:** Choose Public or Private
   - **IMPORTANT:** Do NOT check "Initialize with README" (we already have one!)
4. Click "Create repository"
5. Keep this page open - you'll need the commands shown

### Option B: Using GitHub CLI (Faster if installed)

If you have GitHub CLI (`gh`) installed:

```bash
# Login to GitHub
gh auth login

# Create repository
gh repo create script-to-film-platform --public --source=. --remote=origin

# Push code
git push -u origin main
```

Skip to Step 5 if you used this option!

## Step 4: Connect Local Repo to GitHub

After creating the repo on GitHub, connect it:

```bash
# Add GitHub as the remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/script-to-film-platform.git

# Verify it's added
git remote -v

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

## Step 5: Invite Your Collaborator

### On GitHub Website:

1. Go to your repository: `https://github.com/YOUR_USERNAME/script-to-film-platform`
2. Click "Settings" tab
3. Click "Collaborators and teams" (or just "Collaborators")
4. Click "Add people"
5. Enter your friend's GitHub username or email
6. Select them from the dropdown
7. Click "Add [username] to this repository"

Your friend will receive an email invitation!

### Using GitHub CLI:

```bash
gh repo add-collaborator YOUR_FRIEND_USERNAME
```

## Step 6: Set Up Branch Protection (Recommended)

This prevents accidental direct commits to `main`:

1. Go to repository Settings
2. Click "Branches" in left sidebar
3. Click "Add branch protection rule"
4. Branch name pattern: `main`
5. Enable these settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals** (set to 1)
   - ✅ **Dismiss stale pull request approvals when new commits are pushed**
   - ✅ **Require review from Code Owners** (optional)
6. Click "Create" at the bottom

Now you MUST use Pull Requests - no direct pushes to main!

## Step 7: Your Friend Clones the Repository

Send your friend these instructions:

```bash
# Clone the repository (replace YOUR_USERNAME)
git clone https://github.com/YOUR_USERNAME/script-to-film-platform.git
cd script-to-film-platform

# Configure git (if not already done)
git config --global user.name "Their Name"
git config --global user.email "their.email@example.com"

# Set up backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Copy and configure .env
cp .env.example .env
# Edit .env with their API keys

# Set up frontend
cd frontend
npm install

# Run backend (terminal 1)
cd /path/to/script-to-film-platform
source venv/bin/activate
python -m uvicorn script_to_film.main:app --reload --port 8000

# Run frontend (terminal 2)
cd /path/to/script-to-film-platform/frontend
npm run dev
```

## Step 8: Start Collaborating!

Now you both can use GitHub Flow:

### Example First Feature

**You:**
```bash
git checkout main
git pull origin main
git checkout -b feature/add-export-button
# ... make changes ...
git add .
git commit -m "feat: Add export button to UI"
git push origin feature/add-export-button
# Create PR on GitHub
```

**Your Friend:**
- Reviews your PR on GitHub
- Approves it
- You merge it!

**Both of you:**
```bash
git checkout main
git pull origin main
```

Now you both have the latest code!

## Quick Reference

### Files We Created

- ✅ `CONTRIBUTING.md` - Detailed contribution guidelines
- ✅ `GITHUB_FLOW_GUIDE.md` - Complete GitHub Flow tutorial
- ✅ `.github/pull_request_template.md` - PR template
- ✅ `.github/WORKFLOW_CHEATSHEET.md` - Quick command reference
- ✅ `GIT_SETUP_STEPS.md` - This file!

### Daily Workflow

```bash
# Start of day
git checkout main
git pull origin main
git checkout -b feature/your-feature

# During work
git add .
git commit -m "feat: your change"
git push origin feature/your-feature

# After PR is merged
git checkout main
git pull origin main
```

## Troubleshooting

### "fatal: not a git repository"
```bash
cd /Users/alanballesterossandoval/script-to-film-platform
```

### "Author identity unknown"
Run Step 1 again to configure git user.

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/script-to-film-platform.git
```

### "Permission denied (publickey)"
Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/script-to-film-platform.git
```

## What Happens Next?

1. ✅ You configure git (Step 1)
2. ✅ You create initial commit (Step 2)
3. ✅ You create GitHub repo (Step 3)
4. ✅ You push code to GitHub (Step 4)
5. ✅ You invite your friend (Step 5)
6. ✅ You set up branch protection (Step 6)
7. ✅ Your friend clones and sets up (Step 7)
8. 🚀 You both start building amazing features!

## Need Help?

- Read `CONTRIBUTING.md` for detailed guidelines
- Read `GITHUB_FLOW_GUIDE.md` for step-by-step scenarios
- Check `.github/WORKFLOW_CHEATSHEET.md` for quick commands

---

**You're all set! 🎉**

Everything is configured and ready to go. Just follow the steps above to push to GitHub and start collaborating with your friend!
