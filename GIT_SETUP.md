# Git Setup Instructions

Follow these steps to push your code to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/Nithin11S
2. Click the **"+"** button in the top right
3. Select **"New repository"**
4. Repository name: `agri-robo-tomato` (or any name you prefer)
5. Description: "Tomato Disease Detection System using Deep Learning"
6. Choose **Public** or **Private**
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click **"Create repository"**

## Step 2: Add Remote and Push

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote repository (replace YOUR_USERNAME with Nithin11S)
git remote add origin https://github.com/Nithin11S/agri-robo-tomato.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Verify

1. Go to https://github.com/Nithin11S/agri-robo-tomato
2. Verify all files are uploaded
3. Check that large files (models, training data) are NOT included

## What's Included in Git

✅ **Included:**
- All source code (.py, .jsx files)
- Requirements files
- Configuration files
- Documentation (README, SETUP.md, etc.)
- class_mapping.json (small, useful file)
- Startup scripts

❌ **Excluded (via .gitignore):**
- Model files (*.h5) - too large
- Training data (train/, val/) - too large
- Virtual environments (venv/) - each person creates their own
- Node modules (node_modules/) - run `npm install` after clone
- Environment variables (.env) - sensitive data
- IDE files (.vscode/, .idea/)
- OS files (.DS_Store, Thumbs.db)

## For Your Teammate

Your teammate can clone and set up the project:

```bash
# Clone repository
git clone https://github.com/Nithin11S/agri-robo-tomato.git
cd agri-robo-tomato

# Follow SETUP.md for installation instructions
```

They will need to:
1. Create their own virtual environment
2. Install dependencies from requirements.txt
3. Train their own model or download it separately
4. Run `npm install` for frontend

## Updating the Repository

When you make changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "Description of your changes"

# Push
git push origin main
```

## Important Notes

- **Never commit sensitive data** (API keys, passwords, credentials)
- **Never commit large files** (models, datasets) - use Git LFS or external storage
- **Always test before pushing** to main branch
- **Use branches** for new features: `git checkout -b feature/new-feature`

