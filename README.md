# MANAVARTHA-AI
**Multilingual Telugu News RAG Application** (Capstone Project)

## 🚀 Oracle Cloud Deployment (Production)
This repository is configured for **Oracle Cloud Always Free (ARM)** with Zero Downtime updates.

### Quick Start (On Oracle VM)
```bash
# 1. Clone
git clone https://github.com/BHANU2624/MANAVARTHA-AI.git
cd MANAVARTHA-AI

# 2. Deploy (Auto-Install)
bash deploy_oracle.sh
```

### Automation Features
- **Daily Update**: `backend/daily_update.py` (Runs at 2 AM)
- **Zero Downtime**: `backend/rebuild_index.py` (Runs at 3 AM)

