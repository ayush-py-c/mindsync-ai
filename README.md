# MindSync AI

MindSync AI is a full-stack emotion-to-music app.

- Frontend: React web app
- Backend: Django REST API
- Inference: Python ML service (text, speech, facial) in `modal_inference/`

This repository has been reduced to the minimum needed to keep all core features working and deployable.

## Features

- User authentication
- Profile and history
- Text emotion detection
- Speech emotion detection
- Facial emotion detection
- Music recommendations
- Mood feedback and personalization

## Architecture

- Frontend calls backend for auth, profile, history, and text/music proxy flows.
- Frontend calls inference directly for speech and facial uploads.
- Backend proxies selected inference calls to the inference service.

## Repository Structure

- `frontend/` React application
- `backend/` Django API
- `modal_inference/` inference service
- `render.yaml` Render config for backend deployment

## Prerequisites

- Node.js 18+
- Python 3.11+
- A MongoDB connection string
- An inference deployment URL and token

## Local Development

### 1. Start backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://127.0.0.1:8000`.

### 2. Start frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`.

### 3. Start inference service (optional for local full flow)

```bash
cd modal_inference
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Then run using your inference workflow (Modal or equivalent).

## Required Environment Variables

### Backend (`backend/.env`)

- `SECRET_KEY`
- `DEBUG`
- `MONGO_DB_URI`
- `JWT_SIGNING_KEY`
- `MODAL_INFERENCE_URL`
- `MODAL_SERVICE_TOKEN`
- `CORS_ALLOWED_ORIGINS`

### Frontend (Vercel env or `frontend/.env`)

- `REACT_APP_API_URL`
- `REACT_APP_MODAL_API_URL`

### Inference service

Set values required by `modal_inference/config.py`, including auth and model settings.

## Deployment

### Frontend (Vercel)

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `build`
- Set env vars:
  - `REACT_APP_API_URL`
  - `REACT_APP_MODAL_API_URL`

### Backend (Render or Railway)

- Root directory: `backend`
- Install command: `pip install -r requirements.txt`
- Start command: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3`
- Set backend env vars listed above.

You can use `render.yaml` for Render.

### Inference service

Deploy from `modal_inference/` and set:

- `JWT_SIGNING_KEY` (must match backend)
- `MODAL_SERVICE_TOKEN` (must match backend)
- Any model and provider credentials required by `modal_inference`.

## API Surface (high level)

Backend:

- `POST /users/register/`
- `POST /users/login/`
- `GET /users/profile/`
- `POST /api/text_emotion/`
- `POST /api/music_recommendation/`

Inference service:

- `POST /text_emotion`
- `POST /speech_emotion`
- `POST /facial_emotion`
- `POST /music_recommendation`
- `GET /health`

## Notes

- Keep backend and inference JWT/token secrets aligned.
- If inference is unavailable, emotion features will degrade or fail.
- This repo intentionally excludes old training/analytics/infra folders to stay minimal and deployable.

## License

See `LICENSE`.
