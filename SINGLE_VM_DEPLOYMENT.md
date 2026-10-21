# MindSync AI - Single VM Deployment (Azure)
==============================================

Deploy the **entire MindSync AI stack** on **one Azure VM** (Standard D2as v4: 2 vCPU, 8 GB RAM) using Docker Compose.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure VM (D2as v4)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Nginx     │  │  Frontend   │  │      Backend        │  │
│  │  (80/443)   │──▶│  (React)    │  │     (Django)        │  │
│  └─────────────┘  └─────────────┘  └──────────┬──────────┘  │
│         ▲                                     │             │
│         │                    ┌────────────────┘             │
│         │                    ▼                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Inference (FastAPI + ML)               │    │
│  │  • Text Emotion (BERT)                              │    │
│  │  • Speech Emotion (MFCC + sklearn)                  │    │
│  │  • Facial Emotion (FER + MTCNN)                     │    │
│  │  • Deezer Recommendations                           │    │
│  └─────────────────────────────────────────────────────┘    │
│         ▲                    ▲                              │
│         │                    │                              │
│  ┌──────┴──────┐    ┌─────────┴─────────┐                  │
│  │  MongoDB    │    │   Certbot         │                  │
│  │  (data)     │    │   (SSL)           │                  │
│  └─────────────┘    └───────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## Resource Requirements (D2as v4 = 2 vCPU, 8 GB RAM)

| Service | CPU Limit | Memory Limit | Memory Reserved |
|---------|-----------|--------------|-----------------|
| Nginx | - | 128 MB | 64 MB |
| Frontend | - | 256 MB | 128 MB |
| Backend | - | 2 GB | 1 GB |
| **Inference** | - | **5 GB** | **3 GB** |
| MongoDB | - | 1 GB | 512 MB |
| **Total** | **2 vCPU** | **~8.4 GB** | **~4.7 GB** |

⚠️ **Tight fit** - Inference uses ~5 GB for all 3 models (BERT + TF/FER + Speech). The VM has 8 GB total. Swap is recommended.

## Quick Start

### 1. Prerequisites
- Azure CLI (`az login`)
- Hugging Face model repo with `model.safetensors` + tokenizer
- (Optional) Domain name for SSL

### 2. Generate Secrets
```bash
./scripts/generate-vm-secrets.sh
# Edit .env.vm:
#   HF_TEXT_MODEL_REPO=your-username/mindsync-text-emotion
#   DOMAIN=your-domain.com  (or leave as localhost)
```

### 3. Deploy
```bash
# With domain (auto SSL):
./scripts/deploy-vm.sh mindsync-rg mindsync-vm eastus mindsync.example.com

# Without domain (IP only, no SSL):
./scripts/deploy-vm.sh mindsync-rg mindsync-vm eastus
```

### 4. Access
- **With domain**: `https://your-domain.com`
- **Without domain**: `http://<VM_PUBLIC_IP>`

## What Gets Created

```
Resource Group: mindsync-rg
  └── VM: mindsync-vm (Standard D2as v4, Ubuntu 22.04)
        ├── Docker + Docker Compose
        ├── Nginx (reverse proxy + SSL)
        ├── 4 App Containers (frontend, backend, inference, mongodb)
        └── Certbot (auto Let's Encrypt)
```

## Files

```
docker-compose.prod.yml     # All services
frontend/Dockerfile.prod    # React + nginx
backend/Dockerfile.prod     # Django + gunicorn
modal_inference/Dockerfile.prod  # FastAPI + ML models
modal_inference/entrypoint.prod.sh
nginx/nginx.prod.conf       # Reverse proxy + SSL + rate limits
scripts/deploy-vm.sh        # One-command deploy
scripts/generate-vm-secrets.sh
.env.vm                     # Secrets (generated)
```

## ML Models on Single VM

The inference service downloads the **text emotion model** (~400 MB) from Hugging Face at first startup (2-3 min). All models loaded in memory:

- **Text**: BERT classifier (~500 MB)
- **Facial**: FER + MTCNN (TF/Keras) (~2 GB)
- **Speech**: MFCC + sklearn (~50 MB)
- **Overhead**: Python + TF + PyTorch (~2 GB)

Total: ~4.5 GB RAM for inference alone.

## Management Commands

```bash
# SSH to VM
ssh azureuser@<PUBLIC_IP>

# View logs
cd /opt/mindsync && docker compose -f docker-compose.prod.yml logs -f

# Restart a service
docker compose -f docker-compose.prod.yml restart inference

# Update images
docker compose -f docker-compose.prod.yml pull && docker compose -f docker-compose.prod.yml up -d

# Check resources
docker stats

# Renew SSL
sudo certbot renew
```

## Cost Estimate (Azure, East US)

| Resource | Monthly Cost (Pay-as-you-go) |
|----------|------------------------------|
| Standard D2as v4 (2 vCPU, 8 GB) | ~$70/month |
| OS Disk (128 GB SSD) | ~$12/month |
| Public IP | ~$3/month |
| **Total** | **~$85/month** |

*Reserved instances or Azure Savings Plan can reduce by 30-65%.*

## Troubleshooting

**Inference OOM / Container killed:**
- Enable swap: `sudo fallocate -l 4G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile`
- Add to `/etc/fstab`: `/swapfile none swap sw 0 0`

**Model download fails:**
```bash
ssh azureuser@<IP>
docker exec -it mindsync-inference python3 -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='your-username/mindsync-text-emotion', local_dir='/models/text_emotion_model')
"
```

**Health checks failing:**
```bash
docker compose -f docker-compose.prod.yml logs inference
docker compose -f docker-compose.prod.yml logs backend
```

**Port conflicts:**
- Ensure ports 80, 443, 8000, 8001, 27017 are free on host

## Security Notes

- All secrets in `.env.vm` → written to `/opt/mindsync/.env` on VM (root:root, 600)
- Nginx rate limits: API 30/s, Auth 10/min, Media 5/s
- Internal services not exposed externally
- JWT signing key shared between backend ↔ inference
- MongoDB only accessible internally

## Cleanup

```bash
az group delete -n mindsync-rg --yes --no-wait
```