#!/usr/bin/env bash
# MindSync AI Inference - Production Entrypoint
# Downloads HF model at startup, starts uvicorn

set -euo pipefail

MODELS_DIR="/models"
TEXT_EMOTION_DIR="${MODELS_DIR}/text_emotion_model"
ASSETS_DIR="/app/assets"
TEXT_ASSETS_DIR="${ASSETS_DIR}/text_emotion_model"

echo "=== MindSync AI Inference Starting ==="
echo "Models: ${MODELS_DIR}"
echo "HF Repo: ${HF_TEXT_MODEL_REPO:-not set}"

mkdir -p "${TEXT_EMOTION_DIR}"

if [[ -n "${HF_TEXT_MODEL_REPO:-}" ]]; then
    if [[ ! -f "${TEXT_EMOTION_DIR}/model.safetensors" ]]; then
        echo "Downloading model from HF..."
        python3 - <<'PYEOF'
import os, shutil
from huggingface_hub import snapshot_download

repo = os.getenv("HF_TEXT_MODEL_REPO")
token = os.getenv("HF_TOKEN")
dest = os.getenv("TEXT_EMOTION_DIR")
assets = os.getenv("TEXT_ASSETS_DIR")

try:
    snapshot_download(
        repo_id=repo, local_dir=dest, token=token or None,
        allow_patterns=["*.json", "*.txt", "*.safetensors", "*.bin", "*.model"]
    )
    if os.path.isdir(assets):
        for name in os.listdir(assets):
            src = os.path.join(assets, name)
            dst = os.path.join(dest, name)
            if os.path.isfile(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
    print(f"Model ready: {sorted(os.listdir(dest))}")
except Exception as e:
    print(f"Download failed: {e}")
PYEOF
    else
        echo "Model exists, skipping download"
    fi
else
    echo "WARNING: HF_TEXT_MODEL_REPO not set"
fi

echo "Starting uvicorn on ${HOST:-0.0.0.0}:${PORT:-8001}"
exec uvicorn service:create_app \
    --host "${HOST:-0.0.0.0}" --port "${PORT:-8001}" \
    --workers 1 --factory --log-level info