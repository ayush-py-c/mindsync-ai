#!/usr/bin/env bash
# Entrypoint for the MindSync AI inference container.
# Downloads the text-emotion model from Hugging Face (if not already present),
# then starts the FastAPI server via uvicorn.
#
# Required env vars:
#   HF_TEXT_MODEL_REPO  -- Hugging Face repo containing model.safetensors + tokenizer
#   HF_TOKEN            -- (optional) HF token for private repos
#   JWT_SIGNING_KEY     -- HS256 secret shared with Django backend
#   MODAL_SERVICE_TOKEN -- shared secret for Django->inference trusted calls
#   ALLOWED_ORIGINS     -- comma-separated CORS origins
#   MONGO_DB_URI        -- (optional) MongoDB for metrics persistence
#   Other vars from config.py (METRICS_ENABLED, CACHE_*, RATE_LIMIT_*, etc.)

set -euo pipefail

MODELS_DIR="/models"
TEXT_EMOTION_DIR="${MODELS_DIR}/text_emotion_model"
ASSETS_DIR="/app/assets"
TEXT_ASSETS_DIR="${ASSETS_DIR}/text_emotion_model"

echo "=== MindSync AI Inference Service Starting ==="
echo "Models directory: ${MODELS_DIR}"
echo "Text emotion dir: ${TEXT_EMOTION_DIR}"

# Ensure models directory exists.
mkdir -p "${TEXT_EMOTION_DIR}"

# Download model weights from Hugging Face if missing.
# The HF repo must contain model.safetensors (and optionally config/tokenizer).
# Bundled tokenizer/config assets from the image are copied alongside.
if [[ -n "${HF_TEXT_MODEL_REPO:-}" ]]; then
    if [[ ! -f "${TEXT_EMOTION_DIR}/model.safetensors" ]]; then
        echo "Downloading text-emotion model from HF: ${HF_TEXT_MODEL_REPO}"
        python3 - <<'PYEOF'
import os, shutil
from huggingface_hub import snapshot_download

repo = os.getenv("HF_TEXT_MODEL_REPO")
token = os.getenv("HF_TOKEN")
dest = os.getenv("TEXT_EMOTION_DIR")
assets = os.getenv("TEXT_ASSETS_DIR")

snapshot_download(
    repo_id=repo,
    local_dir=dest,
    token=token or None,
    allow_patterns=["*.json", "*.txt", "*.safetensors", "*.bin", "*.model"],
)

# Merge bundled tokenizer/config assets next to the weights.
if os.path.isdir(assets):
    for name in os.listdir(assets):
        src = os.path.join(assets, name)
        dst = os.path.join(dest, name)
        if os.path.isfile(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"  + copied bundled {name}")

print(f"Model ready at {dest}: {sorted(os.listdir(dest))}")
PYEOF
    else
        echo "Model weights already present, skipping download."
    fi
else
    echo "WARNING: HF_TEXT_MODEL_REPO not set -- text emotion will run in degraded mode."
fi

# Start uvicorn.
echo "Starting FastAPI server on ${HOST}:${PORT}..."
exec uvicorn service:create_app \
    --host "${HOST}" \
    --port "${PORT}" \
    --workers 1 \
    --factory