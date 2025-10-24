# Security Checklist for Public Release

## ✅ Completed

### Secrets Protection
- [x] `.env` is in `.gitignore`
- [x] `.env.example` created with placeholder values (no real credentials)
- [x] Certificate files (`.p12`, `.pem`, `.key`) added to `.gitignore`
- [x] Verified no certificates in repository

### Personal Information
- [x] User paths only in `.env` (which is gitignored)
- [x] No hardcoded passwords in code
- [x] CLAUDE.md contains no sensitive information (only documentation)

### Code Quality
- [x] Python cache (`__pycache__`) in `.gitignore`
- [x] Cleaned up existing `__pycache__` directories
- [x] Log files (`*.log`, `logs/`) in `.gitignore`
- [x] IDE files (`.vscode/`, `.idea/`) in `.gitignore`

## ⚠️ Before Committing - VERIFY

Before each commit, verify:

```bash
# 1. Check that .env is not staged
git status | grep ".env"
# Should show: nothing (if .env is properly ignored)

# 2. Search for any remaining personal paths (replace 'yourusername' with actual username)
git grep "C:/Users/yourusername" -- ':!.env'
# Should show: nothing (all paths should be in .env only)

# 3. Search for password/credential patterns
git grep -i "password\|secret\|credential" -- ':!.env.example' ':!SECURITY_CHECKLIST.md' ':!CLAUDE.md' ':!README.md' ':!docs/'
# Should show: only documentation references, no actual values

# 4. Check for certificate files
git ls-files | grep -E "\\.p12$|\\.pem$|\\.key$"
# Should show: nothing

# 5. Verify .gitignore is working
git check-ignore .env __pycache__ *.log
# Should show: all three are ignored
```

## 🔍 Manual Review Required

Before pushing to public repository, manually review:

### Configuration Files
- [ ] `.env.example` - Contains NO real values, only examples
- [ ] `CLAUDE.md` - Contains NO personal information
- [ ] Any config files in `input/` directory

### Code Files
- [ ] No hardcoded API endpoints with auth tokens
- [ ] No embedded credentials in connection strings
- [ ] No local file system paths outside of `.env`

### Documentation
- [ ] README contains NO personal information
- [ ] Example paths use placeholders like `/path/to/` or `C:/Users/username/`
- [ ] No screenshots containing personal data

### Output Files
- [ ] `output/` directory - Check for any accidentally committed large files
- [ ] ValueSets contain only LOINC codes and SNOMED IDs (public information)
- [ ] No patient data or PHI in any output

## 📋 Environment Variables - Safe Values

The `.env` file should **never** be committed. The `.env.example` shows structure only:

**Safe (in `.env.example`):**
```env
auth_path =
auth_file =
auth_pw =
loinc_snomed_mapping_path =
loinc_csv_path =
```

**NEVER commit (these stay in your local `.env`):**
```env
auth_path="C:/Users/username/.secrets"  # ❌ Personal path
auth_file="your_name_certificate_2024-10-24.p12"  # ❌ Personal certificate
auth_pw=YourSecretPassword123!  # ❌ Real password!
loinc_snomed_mapping_path="C:/Users/username/terminologies/..."  # ❌ Personal path to downloaded loincsnomed distributions
```

## 🚨 Emergency: If Secrets Were Committed

If secrets were accidentally committed to git history:

1. **DO NOT just delete and recommit** - Secrets remain in git history!

2. **Use git history rewriting:**
```bash
# Remove from history using git filter-branch or BFG Repo Cleaner
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG (recommended, faster):
bfg --delete-files .env
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

3. **Revoke compromised credentials:**
   - Regenerate certificate with new password
   - Update MII OntoServer access if needed

4. **Force push** (destructive, coordinate with team):
```bash
git push origin --force --all
```

## ✨ Best Practices

### For Contributors
- Never commit `.env` files
- Use relative paths when possible
- Document why a path must be absolute
- Use environment variables for all paths

### For Code Reviews
- Check all PR diffs for secrets
- Look for patterns: passwords, tokens, keys, certificates
- Verify `.gitignore` includes new secret types
- Test that examples work without real credentials

### For Automation
- Use GitHub secrets for CI/CD
- Never print environment variables in logs
- Scan commits with secret detection tools (e.g., git-secrets, truffleHog)

## 📚 Additional Resources

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Git Secrets Prevention](https://github.com/awslabs/git-secrets)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

## 🎯 Summary

**The golden rule**: If you're unsure whether something should be committed, **DON'T commit it**. Ask first.

**Quick check before pushing**:
```bash
git diff --cached | grep -iE "password|secret|auth_pw|\.secrets|\.p12"
```
If this shows anything suspicious, **STOP** and review carefully.
