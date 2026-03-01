#!/bin/bash
# Skills GitHub Publisher - Morning Upload Script
# Runs at 6:00 AM daily

set -e

GREEN='\033[0;32m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

SKILLS_SOURCE="$HOME/.openclaw/workspace/skills"
GITHUB_REPO="${GITHUB_REPO:-}"  # Will be set by user
COMMIT_MSG="📚 Daily Skills Update - $(date '+%Y-%m-%d')"

log "🚀 Starting Daily Skills Upload to GitHub"

# Check if GitHub token exists
if [ -z "$GITHUB_TOKEN" ]; then
    log "⚠️ GITHUB_TOKEN not set. Please configure before running."
    exit 1
fi

# Check if repo is configured
if [ -z "$GITHUB_REPO" ]; then
    log "⚠️ GITHUB_REPO not set. Please configure target repository."
    exit 1
fi

# Clone or pull existing repo
TEMP_DIR="/tmp/skills-github-$$"
mkdir -p "$TEMP_DIR"

log "📦 Cloning repository..."
git clone "https://$GITHUB_TOKEN@github.com/$GITHUB_REPO.git" "$TEMP_DIR" 2>/dev/null || {
    log "ℹ️ Repo not found, will create on first push"
    mkdir -p "$TEMP_DIR/.git"
}

# Copy all skills
cd "$TEMP_DIR"
rm -rf skills/* 
mkdir -p skills
cp -r "$SKILLS_SOURCE"/* skills/ 2>/dev/null || true

# Generate README with multi-language index
log "🌐 Generating multi-language README..."
python3 "$HOME/.openclaw/workspace/skills-publisher/scripts/generate-readme.py"

# Git operations
log "📤 Committing changes..."
git add --all
git commit -m "$COMMIT_MSG" --allow-empty || true
git push origin main 2>&1 || {
    log "⚠️ Push failed, may need to configure remote"
}

# Cleanup
rm -rf "$TEMP_DIR"

log "✅ Daily upload complete!"
