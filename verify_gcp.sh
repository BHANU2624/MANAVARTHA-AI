#!/bin/bash

echo "========================================"
echo "🔍 MANAVARTHA AI - GCP VERIFICATION"
echo "========================================"

# 1. Service Status
echo ""
echo "[1] Service Status (Full):"
systemctl status manavartha.service --no-pager

# 2. Memory Check
echo ""
echo "[2] Memory Usage:"
free -h

# 3. Dataset Check
echo ""
echo "[3] Checking Dataset:"
ls -lh backend/data/

# 4. Local Access Test
echo ""
echo "[4] Testing Local API Access:"
curl -I http://localhost:8000/docs

# 5. Cron Jobs
echo ""
echo "[5] Checking Cron Jobs:"
crontab -l

echo ""
echo "========================================"
echo "To test restart stability, run: sudo systemctl restart manavartha.service"
echo "========================================"
