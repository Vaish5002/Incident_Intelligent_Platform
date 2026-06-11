# Git Setup and Branch Management Guide

## 📋 Quick Reference

**Your Branch:** `rag-rca` (Member 3 - AI & RCA Engine)  
**Other Branch to Merge:** `frontend-ui` (Member 4)  
**Main Branch:** `main` or `master`

---

## 🚀 Step-by-Step Instructions

### Step 1: Initial Setup (First Time Only)

```bash
# Navigate to your project
cd d:\Incident_Intelligent_Platform

# Set your git identity (do this once)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Verify it's set
git config user.name
git config user.email
```

### Step 2: Create Initial Commit on Main Branch

```bash
# Make sure you're on master/main
git status

# Commit all Member 3 code
git commit -m "feat: Member 3 - Complete AI & RCA Engine (All 9 Modules)

- Module 1: Gemini Integration
- Module 2: RCA Prompt Engineering
- Module 3: Risk Scoring Engine
- Module 4: RCA Generator
- Module 5: Knowledge Base
- Module 6: Embedding Service
- Module 7: RAG Retrieval
- Module 8: AI Copilot
- Module 9: PDF Generator

Total: 37 API endpoints, 9 services, 61 tests passing"
```

### Step 3: Create Your Branch (rag-rca)

```bash
# Create and switch to your branch
git checkout -b rag-rca

# Verify you're on the new branch
git branch
# You should see: * rag-rca

# Push your branch to remote (if you have a remote repository)
git push -u origin rag-rca
```

### Step 4: Check if frontend-ui Branch Exists

```bash
# List all branches (local and remote)
git branch -a

# If you see 'remotes/origin/frontend-ui', it exists on remote
# If not, your teammate needs to push it first
```

### Step 5: Fetch Latest Changes from Remote

```bash
# Fetch all branches from remote
git fetch origin

# See all available branches
git branch -r
```

### Step 6: Merge frontend-ui into Your Branch

**Option A: If frontend-ui exists on remote**

```bash
# Make sure you're on rag-rca branch
git checkout rag-rca

# Merge frontend-ui branch
git merge origin/frontend-ui

# If there are conflicts, Git will tell you
```

**Option B: If frontend-ui is local only**

```bash
# Make sure you're on rag-rca branch
git checkout rag-rca

# Merge local frontend-ui branch
git merge frontend-ui

# If there are conflicts, Git will tell you
```

### Step 7: Handle Merge Conflicts (if any)

If you get merge conflicts:

```bash
# Git will show which files have conflicts
git status

# Open conflicted files and look for:
<<<<<<< HEAD
Your code
=======
Their code
>>>>>>> frontend-ui

# Edit the file to keep what you want
# Remove the conflict markers (<<<, ===, >>>)

# After resolving all conflicts:
git add .
git commit -m "merge: Integrate frontend-ui into rag-rca branch"
```

### Step 8: Push Your Branch

```bash
# Push your branch with merged changes
git push origin rag-rca
```

---

## 🔧 Common Scenarios

### Scenario 1: frontend-ui Branch Doesn't Exist Yet

**What to do:**
1. Ask your teammate (Member 4) to create and push their branch first
2. They should run:
   ```bash
   git checkout -b frontend-ui
   git add .
   git commit -m "feat: Member 4 - Frontend UI"
   git push -u origin frontend-ui
   ```
3. Then you fetch and merge

### Scenario 2: No Remote Repository Yet

If you haven't set up a remote (GitHub, GitLab, etc.):

```bash
# Create a repository on GitHub/GitLab first
# Then add the remote:
git remote add origin https://github.com/yourusername/smartops-ai.git

# Push main branch
git push -u origin master

# Push your branch
git push -u origin rag-rca
```

### Scenario 3: You Need to Work on Main Branch First

```bash
# Switch to main
git checkout master

# Make changes, then commit
git add .
git commit -m "update: description"

# Switch back to your branch
git checkout rag-rca

# Bring main changes into your branch
git merge master
```

---

## 📝 Recommended Git Workflow for Your Team

### For You (Member 3 - rag-rca branch):

```bash
# 1. Create your branch (done once)
git checkout -b rag-rca
git push -u origin rag-rca

# 2. Work on your code
# ... make changes ...

# 3. Commit your changes
git add .
git commit -m "feat: add new feature"

# 4. Push your branch
git push origin rag-rca

# 5. When ready to merge frontend code
git fetch origin
git merge origin/frontend-ui

# 6. Resolve any conflicts
# ... fix conflicts ...
git add .
git commit -m "merge: integrate frontend-ui"
git push origin rag-rca

# 7. Finally, merge to main
git checkout main
git merge rag-rca
git push origin main
```

### For Member 4 (frontend-ui branch):

```bash
# They should follow similar steps on their branch
git checkout -b frontend-ui
git push -u origin frontend-ui
# ... work and push changes ...
```

---

## 🚨 Common Issues and Solutions

### Issue 1: "fatal: not a git repository"

**Solution:**
```bash
cd d:\Incident_Intelligent_Platform
git init
```

### Issue 2: "Please tell me who you are"

**Solution:**
```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```

### Issue 3: "Branch already exists"

**Solution:**
```bash
# Switch to the existing branch
git checkout rag-rca

# Or delete and recreate (careful!)
git branch -D rag-rca
git checkout -b rag-rca
```

### Issue 4: "Merge conflict"

**Solution:**
1. Git will mark conflicted files
2. Open each file and look for conflict markers
3. Edit to keep what you want
4. Remove markers (`<<<<<<<`, `=======`, `>>>>>>>`)
5. Save and commit:
   ```bash
   git add .
   git commit -m "resolve: merge conflicts"
   ```

### Issue 5: "Failed to push"

**Solution:**
```bash
# Pull first, then push
git pull origin rag-rca
git push origin rag-rca
```

---

## 📂 Project Structure After Merge

After merging, your project should look like:

```
d:\Incident_Intelligent_Platform\
├── backend/                    # Your code (Member 3)
│   ├── ai/                     # 9 services
│   ├── api/                    # 6 routers
│   ├── database/               # DB models
│   ├── schemas/                # Pydantic schemas
│   ├── main.py                 # FastAPI app
│   └── requirements.txt
├── frontend/                   # Member 4's code (after merge)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── .gitignore
└── README.md
```

---

## ✅ Final Checklist

Before merging branches:

- [ ] All your code is committed on `rag-rca` branch
- [ ] Tests are passing
- [ ] Documentation is updated
- [ ] `.gitignore` is properly configured
- [ ] Sensitive data (.env) is not committed
- [ ] You've communicated with Member 4 about the merge

After merging:

- [ ] Conflicts are resolved (if any)
- [ ] Merged code is tested
- [ ] Both backend and frontend work together
- [ ] Changes are pushed to remote
- [ ] Team is notified

---

## 🎯 Quick Commands Summary

```bash
# Setup (once)
git config user.name "Your Name"
git config user.email "your@email.com"

# Create your branch
git checkout -b rag-rca

# Commit changes
git add .
git commit -m "your message"

# Push your branch
git push -u origin rag-rca

# Merge frontend-ui
git fetch origin
git merge origin/frontend-ui

# Handle conflicts if needed
# Edit files → Save → Then:
git add .
git commit -m "merge: integrate frontend"
git push origin rag-rca

# Finally merge to main
git checkout main
git merge rag-rca
git push origin main
```

---

## 📞 Need Help?

If you encounter issues:

1. Check git status: `git status`
2. Check current branch: `git branch`
3. Check remotes: `git remote -v`
4. Check logs: `git log --oneline -10`

---

**Good luck with your merge! 🚀**
