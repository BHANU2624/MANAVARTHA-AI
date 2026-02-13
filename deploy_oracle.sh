#!/bin/bash

# Deployment Script for Oracle Cloud (Ubuntu/Linux)
# Run this on your VM: bash deploy_oracle.sh

echo "🚀 Starting Manavartha AI Deployment..."

# 1. System Updates
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git

# 2. Setup Project
if [ ! -d "MANAVARTHA-AI" ]; then
    echo "📂 Cloning Repository..."
    git clone https://github.com/BHANU2624/MANAVARTHA-AI.git
fi

cd MANAVARTHA-AI

# 3. Setup Python Environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Virtual Env..."
    python3 -m venv venv
fi

# 4. Check Data (Crucial for Oracle)
if [ ! -f "backend/data/all_telugu_chunk_embeddings_clean.csv" ]; then
    echo "❌ ERROR: Dataset NOT FOUND!"
    echo " You MUST upload the dataset manually via SCP."
    echo " Run on your laptop:"
    echo " scp backend/data/all_telugu_chunk_embeddings_clean.csv ubuntu@YOUR_VM_IP:~/MANAVARTHA-AI/backend/data/"
    exit 1
fi
echo "✅ Dataset found."

echo "📦 Installing Dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

# 4. Setup Data Directory
# Ensure chunks directory exists
mkdir -p backend/data/chunks

# 5. Setup Systemd Service
echo "⚙️ Configuring Systemd Service..."
sudo cp manavartha.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable manavartha
sudo systemctl start manavartha

# 6. Setup Cron Jobs (Daily Update & Rebuild)
echo "⏰ Setting up Cron Jobs..."
# Write to temp cron file
crontab -l > mycron
# Daily Update at 2 AM
echo "0 2 * * * cd /home/ubuntu/MANAVARTHA-AI/backend && /home/ubuntu/MANAVARTHA-AI/venv/bin/python daily_update.py >> /home/ubuntu/MANAVARTHA-AI/backend/cron_update.log 2>&1" >> mycron
# Rebuild Index at 3 AM
echo "0 3 * * * cd /home/ubuntu/MANAVARTHA-AI/backend && /home/ubuntu/MANAVARTHA-AI/venv/bin/python rebuild_index.py >> /home/ubuntu/MANAVARTHA-AI/backend/cron_rebuild.log 2>&1" >> mycron
# Install new cron file
crontab mycron
rm mycron

echo "✅ Deployment Complete!"
echo "🌐 Your app should be running at http://YOUR_VM_IP:8000"
echo "📜 Check status: sudo systemctl status manavartha"
