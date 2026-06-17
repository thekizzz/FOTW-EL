#!/bin/bash
# deploy.sh — build + push FOTW-EL lên GitHub Pages (private repo)
set -e
cd "$(dirname "$0")"
python3 build.py
git add -A
TS=$(TZ=Asia/Ho_Chi_Minh date '+%H:%M · %d/%m/%Y (ICT)')
git commit -m "${1:-update} — $TS" 2>&1 | tail -1 || echo "nothing to commit"
git push -u origin main 2>&1 | tail -2
echo "pushed ✅  $TS"
