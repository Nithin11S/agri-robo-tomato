# GitHub Authentication Fix

You're getting a permission error because Windows is using cached credentials for a different GitHub account.

## Solution: Use Personal Access Token

GitHub no longer accepts passwords. You need to use a Personal Access Token (PAT).

### Step 1: Create Personal Access Token

1. Go to GitHub: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `agri-robo-tomato`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (if you plan to use GitHub Actions)
5. Click **"Generate token"**
6. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)

### Step 2: Update Remote URL with Token

Replace `YOUR_TOKEN` with your actual token:

```bash
# Remove old remote
git remote remove origin

# Add remote with token (replace YOUR_TOKEN)
git remote add origin https://YOUR_TOKEN@github.com/Nithin11S/agri-robo-tomato.git

# Or use this format (Git will prompt for token)
git remote set-url origin https://github.com/Nithin11S/agri-robo-tomato.git
```

### Step 3: Push with Token

When you push, Git will prompt for credentials:
- **Username:** `Nithin11S`
- **Password:** `YOUR_TOKEN` (paste your token here, not your password)

```bash
git push -u origin main
```

## Alternative: Use SSH (Recommended)

SSH is more secure and doesn't require tokens for each push.

### Setup SSH Key

1. **Check if you have SSH key:**
   ```bash
   ls ~/.ssh/id_rsa.pub
   ```

2. **Generate SSH key (if needed):**
   ```bash
   ssh-keygen -t ed25519 -C "nithins221@gmail.com"
   # Press Enter for default location
   # Set a passphrase (optional but recommended)
   ```

3. **Copy public key:**
   ```bash
   # Windows PowerShell
   cat ~/.ssh/id_ed25519.pub | clip
   
   # Or manually copy from: C:\Users\nithi\.ssh\id_ed25519.pub
   ```

4. **Add to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click **"New SSH key"**
   - Title: `My PC` or `Windows Laptop`
   - Key: Paste your public key
   - Click **"Add SSH key"**

5. **Update remote to use SSH:**
   ```bash
   git remote set-url origin git@github.com:Nithin11S/agri-robo-tomato.git
   ```

6. **Test SSH connection:**
   ```bash
   ssh -T git@github.com
   # Should say: "Hi Nithin11S! You've successfully authenticated..."
   ```

7. **Push:**
   ```bash
   git push -u origin main
   ```

## Clear Windows Credentials (If Still Having Issues)

If you still get permission errors, clear Windows Credential Manager:

1. Open **Control Panel** → **Credential Manager**
2. Go to **Windows Credentials**
3. Find entries for `git:https://github.com`
4. Click **Remove** or **Edit** to update
5. Try pushing again

Or use command line:
```bash
# Clear GitHub credentials
cmdkey /list | findstr git
cmdkey /delete:git:https://github.com
```

## Quick Fix (HTTPS with Token)

If you just want to push quickly:

```bash
# Update remote URL
git remote set-url origin https://github.com/Nithin11S/agri-robo-tomato.git

# Push (will prompt for credentials)
git push -u origin main
# Username: Nithin11S
# Password: YOUR_PERSONAL_ACCESS_TOKEN
```

## Verify Setup

```bash
# Check remote URL
git remote -v

# Check git config
git config user.name
git config user.email

# Should show:
# user.name=Nithin11S
# user.email=nithins221@gmail.com
```

