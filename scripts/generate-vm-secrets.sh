#!/usr/bin/env bash
# MindSync AI - Generate VM Deployment Secrets
# =============================================
# Creates .env.vm with all required secrets for deploy-vm.sh

set -euo pipefail

cat <<'EOF' > .env.vm
# MindSync AI - Single VM Deployment Secrets
# ============================================
# Generated: $(date)
# KEEP SECURE - NEVER COMMIT TO GIT!

# ---- Hugging Face Model (REQUIRED) ----
# Create repo at huggingface.co, upload model.safetensors + tokenizer
HF_TEXT_MODEL_REPO=your-username/mindsync-text-emotion
HF_TOKEN=

# ---- Core Secrets (GENERATED) ----
SECRET_KEY=GENERATED_SECRET_KEY
JWT_SIGNING_KEY=GENERATED_JWT_KEY
MODAL_SERVICE_TOKEN=GENERATED_SERVICE_TOKEN

# ---- Domain (REQUIRED for SSL) ----
# Set to your domain (e.g., mindsync.example.com)
# Leave as localhost for IP-only access (no SSL)
DOMAIN=localhost
EOF

# Generate actual secrets
python3 -c "
import secrets, re
with open('.env.vm', 'r') as f:
    content = f.read()
content = re.sub(r'GENERATED_SECRET_KEY', secrets.token_urlsafe(64), content)
content = re.sub(r'GENERATED_JWT_KEY', secrets.token_urlsafe(64), content)
content = re.sub(r'GENERATED_SERVICE_TOKEN', secrets.token_urlsafe(32), content)
with open('.env.vm', 'w') as f:
    f.write(content)
"

echo "Created .env.vm with generated secrets"
echo
echo "EDIT .env.vm AND SET:"
echo "  1. HF_TEXT_MODEL_REPO=your-username/mindsync-text-emotion"
echo "  2. DOMAIN=your-domain.com (or leave as localhost for IP access)"
echo
echo "Then run: ./scripts/deploy-vm.sh mindsync-rg mindsync-vm eastus your-domain.com"