#!/bin/bash
# Script to completely clean Git history of sensitive files

echo "WARNING: This will rewrite Git history!"
echo "Make sure you have a backup of your code."
echo ""

# Remove sensitive files from ALL commits in history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env \
   .hypothesis -r \
   .claude -r \
   logs/app.log" \
  --prune-empty --tag-name-filter cat -- --all

echo "History cleaned locally. Now force push to overwrite remote:"
echo "git push origin --force --all"
echo "git push origin --force --tags"