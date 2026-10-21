#!/usr/bin/env bash
# MindSync AI - Single VM Deployment to Azure
# ============================================
# Provisions a Standard D2as v4 VM (2 vCPU, 8 GB RAM)
# Runs everything via Docker Compose
#
# Usage:
#   ./scripts/deploy-vm.sh [resource-group] [vm-name] [location] [domain]
#   ./scripts/deploy-vm.sh mindsync-rg mindsync-vm eastus mindsync.example.com

set -euo pipefail

# ---- Config ----
RESOURCE_GROUP="${1:-mindsync-rg}"
VM_NAME="${2:-mindsync-vm}"
LOCATION="${3:-eastus}"
DOMAIN="${4:-}"  # Optional: your-domain.com for SSL
ADMIN_USER="azureuser"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ---- Load secrets ----
ENV_FILE="$(dirname "$0")/../.env.vm"
if [[ -f "$ENV_FILE" ]]; then
    log_info "Loading secrets from $ENV_FILE"
    set -a; source "$ENV_FILE"; set +a
else
    log_error "Missing $ENV_FILE. Run ./scripts/generate-vm-secrets.sh first"
    exit 1
fi

# Validate required
for var in SECRET_KEY JWT_SIGNING_KEY MODAL_SERVICE_TOKEN HF_TEXT_MODEL_REPO; do
    [[ -z "${!var:-}" ]] && { log_error "$var not set in $ENV_FILE"; exit 1; }
done

# Check Azure login
az account show >/dev/null 2>&1 || { log_error "Run: az login"; exit 1; }

log_info "========================================"
log_info "  MindSync AI - Single VM Deploy"
log_info "  VM: $VM_NAME (Standard D2as v4)"
log_info "  RG: $RESOURCE_GROUP"
log_info "  Location: $LOCATION"
[[ -n "$DOMAIN" ]] && log_info "  Domain: $DOMAIN"
log_info "========================================"

# ---- 1. Create Resource Group ----
log_info "Creating resource group..."
az group create -n "$RESOURCE_GROUP" -l "$LOCATION" -o none
log_success "Resource group ready"

# ---- 2. Create VM with cloud-init ----
log_info "Creating VM ($VM_NAME)..."
CLOUD_INIT="$(dirname "$0")/cloud-init.yml"

# Build cloud-init with substituted values
  cat > /tmp/cloud-init.yml <<EOF
#cloud-config
package_update: true
packages:
  - docker.io
  - docker-compose-plugin
  - nginx
  - certbot
  - python3-certbot-nginx
  - git
  - curl
  - jq

write_files:
  - path: /opt/mindsync/.env
    owner: root:root
    permissions: '0600'
    content: |
      SECRET_KEY=${SECRET_KEY}
      JWT_SIGNING_KEY=${JWT_SIGNING_KEY}
      MODAL_SERVICE_TOKEN=${MODAL_SERVICE_TOKEN}
      HF_TEXT_MODEL_REPO=${HF_TEXT_MODEL_REPO}
      HF_TOKEN=${HF_TOKEN:-}
      DOMAIN=${DOMAIN:-localhost}

  - path: /opt/mindsync/docker-compose.prod.yml
    owner: root:root
    permissions: '0644'
    content: |
$(sed 's/^/      /' "$(dirname "$0")/../docker-compose.prod.yml")

  - path: /opt/mindsync/nginx/nginx.prod.conf
    owner: root:root
    permissions: '0644'
    content: |
$(sed "s/\\\${DOMAIN}/${DOMAIN:-localhost}/g" "$(dirname "$0")/../nginx/nginx.prod.conf" | sed 's/^/      /')

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker azureuser
  - mkdir -p /opt/mindsync/certbot/conf /opt/mindsync/certbot/www
  - cd /opt/mindsync && docker compose -f docker-compose.prod.yml pull
  - cd /opt/mindsync && docker compose -f docker-compose.prod.yml up -d
  - |
    if [[ -n "${DOMAIN}" && "${DOMAIN}" != "localhost" ]]; then
      sleep 30
      certbot --nginx -d ${DOMAIN} --non-interactive --agree-tos -m admin@${DOMAIN} --redirect || true
    fi

EOF

az vm create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$VM_NAME" \
    --image Ubuntu2204 \
    --size Standard_D2as_v4 \
    --admin-username "$ADMIN_USER" \
    --generate-ssh-keys \
    --custom-data /tmp/cloud-init.yml \
    --public-ip-sku Standard \
    --output none

log_success "VM created, waiting for provisioning..."

# ---- 3. Wait for VM to be ready ----
log_info "Waiting for VM to be ready (this takes 3-5 minutes)..."
az vm wait --resource-group "$RESOURCE_GROUP" --name "$VM_NAME" --created --output none

# Get public IP
PUBLIC_IP=$(az vm show -g "$RESOURCE_GROUP" -n "$VM_NAME" -d --query publicIps -o tsv)
log_success "VM ready at $PUBLIC_IP"

# ---- 4. Wait for Docker Compose to start ----
log_info "Waiting for containers to start (model download takes 2-3 min)..."
sleep 60

# Wait for health checks
for i in {1..20}; do
    if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$ADMIN_USER@$PUBLIC_IP" \
        "cd /opt/mindsync && docker compose -f docker-compose.prod.yml ps --format json" 2>/dev/null | grep -q '"Health":"healthy"'; then
        log_success "Containers are healthy"
        break
    fi
    log_info "Waiting for health checks... ($i/20)"
    sleep 30
done

# ---- 5. SSL Setup (if domain provided) ----
if [[ -n "$DOMAIN" && "$DOMAIN" != "localhost" ]]; then
    log_info "Setting up SSL for $DOMAIN..."
    ssh -o StrictHostKeyChecking=no "$ADMIN_USER@$PUBLIC_IP" \
        "sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN --redirect" || log_warning "SSL setup failed, run manually"
fi

# ---- 6. Verify ----
log_info "Verifying deployment..."
FRONTEND_URL="https://${DOMAIN:-$PUBLIC_IP}"
if curl -sf "$FRONTEND_URL/health" >/dev/null; then
    log_success "Frontend: OK"
else
    log_warning "Frontend health check failed"
fi

BACKEND_URL="$FRONTEND_URL/api/health/"
if curl -sf "$BACKEND_URL" >/dev/null; then
    log_success "Backend API: OK"
else
    log_warning "Backend health check failed"
fi

echo
log_success "=== Deployment Complete ==="
echo "Frontend: $FRONTEND_URL"
echo "Backend:  $FRONTEND_URL/api/"
echo "SSH:      ssh $ADMIN_USER@$PUBLIC_IP"
echo
echo "Manage:   ssh $ADMIN_USER@$PUBLIC_IP 'cd /opt/mindsync && docker compose -f docker-compose.prod.yml logs -f'"