#!/bin/bash

# Deployment Script for Google Cloud Platform (GCP)
# Run this on your GCP VM: bash deploy_gcp.sh

echo "🚀 Starting Manavartha AI Deployment on GCP..."

# Detect User and Path
CURRENT_USER=$(whoami)
User_Home=$HOME
PROJECT_DIR="$User_Home/MANAVARTHA-AI"
BACKEND_DIR="$PROJECT_DIR/backend"
VENV_DIR="$PROJECT_DIR/venv"

echo "📍 Detected User: $CURRENT_USER"
echo "📍 Project Directory: $PROJECT_DIR"

# 1. System Updates
echo "🔄 Updating System..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git

# 1.5 Setup Swap (Crucial for 8GB RAM)
if ! sudo swapon --show | grep -q "/swapfile"; then
    echo "🧠 Creating 4GB Swap File..."
    sudo fallocate -l 4G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ Swap Created."
else
    echo "✅ Swap already exists."
fi


# 2. Setup Project
if [ ! -d "$PROJECT_DIR" ]; then
    echo "📂 Cloning Repository..."
    git clone https://github.com/BHANU2624/MANAVARTHA-AI.git
fi

cd "$PROJECT_DIR" || exit

# 3. Setup Python Environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Virtual Env..."
    python3 -m venv venv
fi

# 4. Check Data (Crucial)
if [ ! -f "backend/data/all_telugu_chunk_embeddings_clean.csv" ]; then
    echo "❌ ERROR: Dataset NOT FOUND!"
    echo " You MUST upload the dataset manually via SCP."
    echo " Run on your laptop:"
    echo " scp backend/data/all_telugu_chunk_embeddings_clean.csv $CURRENT_USER@YOUR_VM_IP:~/MANAVARTHA-AI/backend/data/"
    exit 1
fi
echo "✅ Dataset found."

echo "📦 Installing Dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
# Force reinstall some critical libs if needed
# pip install --force-reinstall numpy faiss-cpu

# 5. Setup Data Directory
mkdir -p backend/data/chunks

# 6. Generate Systemd Service Dynamically
echo "⚙️ Generating Systemd Service..."
SERVICE_FILE="manavartha.service"
cat <<EOF > $SERVICE_FILE
[Unit]
Description=Manavartha AI Backend Service (GCP)
After=network.target

[Service]
User=$CURRENT_USER
WorkingDirectory=$BACKEND_DIR
ExecStart=$VENV_DIR/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
EnvironmentFile=$BACKEND_DIR/.env

[Install]
WantedBy=multi-user.target
EOF

echo "⚙️ Configuring Systemd Service..."
sudo mv $SERVICE_FILE /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable manavartha
sudo systemctl start manavartha

# 7. Setup Cron Jobs (Daily Update & Rebuild)
echo "⏰ Setting up Cron Jobs..."
crontab -l > mycron 2>/dev/null
# Remove existing lines to avoid duplicates
sed -i '/daily_update.py/d' mycron
sed -i '/rebuild_index.py/d' mycron

# Daily Update at 2 AM
echo "0 2 * * * cd $BACKEND_DIR && $VENV_DIR/bin/python daily_update.py >> $BACKEND_DIR/cron_update.log 2>&1" >> mycron
# Rebuild Index at 3 AM
echo "0 3 * * * cd $BACKEND_DIR && $VENV_DIR/bin/python rebuild_index.py >> $BACKEND_DIR/cron_rebuild.log 2>&1" >> mycron

# Install new cron file
crontab mycron
rm mycron

echo "✅ Deployment Complete!"
echo "🌐 Your app should be running at http://YOUR_VM_IP:8000"
echo "📜 Check status: sudo systemctl status manavartha"
