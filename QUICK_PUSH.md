# Quick Push to GitHub - Step by Step

## The Problem
Windows is using cached credentials for account `nithin-17102004` but you need to push to `Nithin11S`.

## Quick Solution (5 minutes)

### Option 1: Use Personal Access Token (Easiest)

1. **Create Token on GitHub:**
   - Go to: https://github.com/settings/tokens/new
   - Name: `agri-robo-push`
   - Expiration: `90 days` (or `No expiration` for convenience)
   - Check: ✅ `repo` (Full control)
   - Click **"Generate token"**
   - **COPY THE TOKEN** (starts with `ghp_...`)

2. **Clear Old Credentials:**
   ```powershell
   cmdkey /delete:git:https://github.com
   ```

3. **Push with Token:**
   ```powershell
   git push -u origin main
   ```
   When prompted:
   - **Username:** `Nithin11S`
   - **Password:** `YOUR_TOKEN_HERE` (paste the token, not your password)

### Option 2: Update Remote URL with Token (No Prompts)

```powershell
# Remove old remote
git remote remove origin

# Add with token (replace YOUR_TOKEN with actual token)
git remote add origin https://YOUR_TOKEN@github.com/Nithin11S/agri-robo-tomato.git

# Push
git push -u origin main
```

**⚠️ Security Note:** This stores token in git config. Use Option 1 for better security.

### Option 3: Use GitHub CLI (Recommended for Future)

```powershell
# Install GitHub CLI
winget install GitHub.cli

# Authenticate
gh auth login

# Push
git push -u origin main
```

## Verify Everything is Correct

```powershell
# Check git config
git config user.name
git config user.email
# Should show: Nithin11S and nithins221@gmail.com

# Check remote
git remote -v
# Should show: https://github.com/Nithin11S/agri-robo-tomato.git
```

## If You Still Get Errors

1. **Make sure repository exists on GitHub:**
   - Go to: https://github.com/Nithin11S
   - Create repository: `agri-robo-tomato` (if not exists)

2. **Check repository permissions:**
   - Make sure you're logged into GitHub as `Nithin11S`
   - Repository should be under `Nithin11S` account

3. **Try SSH instead:**
   - See `GITHUB_AUTH.md` for SSH setup

