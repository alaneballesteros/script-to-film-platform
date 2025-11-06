# GitHub Flow - Quick Cheat Sheet

## Starting a New Feature

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

## Making Changes

```bash
# Make your changes in your editor
git status                    # See what changed
git add .                     # Stage all changes
git commit -m "feat: description"
git push origin feature/your-feature-name
```

## Creating Pull Request

1. Go to GitHub repository
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Fill out template
5. Assign reviewer
6. Click "Create pull request"

## After PR is Merged

```bash
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

## Keep Branch Updated

```bash
git checkout feature/your-branch
git pull origin main
```

## Common Commands

| Command | What it does |
|---------|-------------|
| `git status` | Check current state |
| `git branch` | List branches |
| `git checkout branch-name` | Switch branch |
| `git pull origin main` | Update main |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Commit |
| `git push origin branch-name` | Push to GitHub |
| `git log --oneline` | View history |

## Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code improvements
- `test/` - Tests

## Commit Message Format

```
<type>: <description>

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
```bash
git commit -m "feat: Add user authentication"
git commit -m "fix: Resolve CORS error"
git commit -m "docs: Update API documentation"
```

## Resolving Conflicts

```bash
git pull origin main
# Fix conflicts in editor
git add .
git commit -m "Merge main and resolve conflicts"
git push origin feature/your-branch
```

## Emergency: Undo Last Commit

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes completely
git reset --hard HEAD
```

## Pull Someone Else's Branch

```bash
git fetch origin
git checkout feature/their-branch
# Test it
git checkout your-branch  # Go back
```
