#!/bin/bash

echo "========================================"
echo "🔍 MANAVARTHA AI - ORACLE VERIFICATION"
echo "========================================"

# 1. Service Status
echo ""
echo "[1] Checking Service Status..."
SERVICE_STATUS=$(systemctl is-active manavartha.service)
echo "Status: $SERVICE_STATUS"
if [ "$SERVICE_STATUS" != "active" ]; then
    echo "❌ Service is NOT active!"
    systemctl status manavartha.service --no-pager
else
    echo "✅ Service is running."
fi

# 2. Memory Check
echo ""
echo "[2] Memory Usage:"
free -h | grep Mem

# 3. Dataset Check
echo ""
echo "[3] Checking Dataset:"
DATA_FILE="backend/data/all_telugu_chunk_embeddings_clean.csv"
if [ -f "$DATA_FILE" ]; then
    SIZE=$(ls -lh "$DATA_FILE" | awk '{print $5}')
    echo "✅ Dataset found. Size: $SIZE"
else
    echo "❌ Dataset ($DATA_FILE) NOT FOUND."
fi

# 4. Logs Check (FAISS)
echo ""
echo "[4] Checking Recent Logs for Index Load:"
journalctl -u manavartha.service -n 50 --no-pager | grep -E "Loading pre-built index|Dataset loaded" | tail -n 5

# 5. Local Access Test
echo ""
echo "[5] Testing Local API Access:"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
if [ "$HTTP_CODE" == "200" ]; then
    echo "✅ Local Access (docs): OK (200)"
else
    echo "❌ Local Access FAILED (Code: $HTTP_CODE)"
fi

# 6. Cron Jobs
echo ""
echo "[6] Checking Cron Jobs:"
crontab -l

echo ""
echo "========================================"
echo "To test restart stability, run: sudo systemctl restart manavartha.service"
echo "========================================"
