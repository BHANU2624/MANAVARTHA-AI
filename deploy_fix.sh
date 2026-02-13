#!/bin/bash

# MANAVARTHA AI - Safe Backend Recovery Script
# This script switches the production server from the limited RAG-only version
# to the Full-Feature Backend (Auth + Chat History + RAG).

echo "🚀 Starting Safe Backend Recovery..."

# 1. Define Paths
PROJECT_DIR="$HOME/MANAVARTHA-AI"
BACKEND_DIR="$PROJECT_DIR/backend"
BACKUP_DIR="$PROJECT_DIR/backend_rag_backup_$(date +%F_%H%M)"
VENV_DIR="$PROJECT_DIR/venv"

# 2. Backup Current State (Code Only, Preserving Data)
echo "📦 Backing up current backend to $BACKUP_DIR..."
# Create backup dir
mkdir -p "$BACKUP_DIR"
# Copy all files from backend to backup, EXCLUDING data directory to save space/time
rsync -av --exclude='data' "$BACKEND_DIR/" "$BACKUP_DIR/"

echo "✅ Backup Complete."

# 3. Pull Latest Full-Feature Code
echo "⬇️ Pulling latest code..."
cd "$PROJECT_DIR" || exit
git fetch origin main
git reset --hard origin/main

# 4. Restore/Protect Data (Safety Net)
# git reset should NOT touch backend/data because it's in .gitignore (verified previously)
# But let's verify key files exist.
if [ ! -f "$BACKEND_DIR/main.py" ]; then
    echo "❌ CRITICAL: main.py not found after pull!"
    exit 1
fi

# 5. Update Dependencies (Critical for Auth)
echo "🐍 Updating Dependencies..."
source "$VENV_DIR/bin/activate"
pip install -r "$BACKEND_DIR/requirements.txt"

# 6. Ensure Service uses main.py (Full App) not server.py
echo "⚙️ Configuring Service..."
SERVICE_FILE="manavartha.service"
# Re-write service file to guarantee it points to 'main:app'
cat <<EOF > $SERVICE_FILE
[Unit]
Description=Manavartha AI Backend Service (Full Feature)
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$BACKEND_DIR
ExecStart=$VENV_DIR/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
EnvironmentFile=$BACKEND_DIR/.env

[Install]
WantedBy=multi-user.target
EOF

sudo mv $SERVICE_FILE /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart manavartha

# 7. Verification Logs
echo "✅ Backend Restarted."
echo "📜 Checking Status..."
sudo systemctl status manavartha --no-pager
echo " "
echo "🎉 DEPLOYMENT COMPLETE."
echo "   - Backup saved to: $BACKUP_DIR"
echo "   - Active App: main:app"
