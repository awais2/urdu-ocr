# Nuskha — Urdu Newspaper OCR

Full-stack app that extracts Urdu (Nastaliq) text from newspaper scans using
GPT-4o vision, with a FastAPI backend, React + TypeScript frontend, and
MongoDB for extraction history.

## Architecture

```
urdu-ocr-app/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entrypoint, CORS, lifespan
│   │   ├── config.py               # Settings loaded from .env
│   │   ├── api/routes/
│   │   │   ├── ocr.py              # POST /api/ocr/extract
│   │   │   └── documents.py        # GET/DELETE /api/documents
│   │   ├── core/preprocessing.py   # Image preprocessing (separate module)
│   │   ├── services/ocr_service.py # GPT-4o vision call
│   │   ├── db/mongodb.py           # Async Mongo (Motor) connection
│   │   └── models/schemas.py       # Pydantic schemas
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx                 # Page composition + state
│   │   ├── api/client.ts           # Typed fetch client
│   │   ├── components/             # UploadZone, ResultPanel, HistoryList
│   │   ├── types/index.ts
│   │   └── index.css               # Design tokens + styles
│   └── .env.example
├── docker-compose.yml              # Local MongoDB
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for MongoDB) or a local/Atlas MongoDB instance
- An OpenAI API key

## Setup

### 1. MongoDB

```bash
docker compose up -d
```

(or set `MONGODB_URI` in `backend/.env` to your Atlas connection string)

### 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then edit .env and paste your OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env        # VITE_API_URL defaults to http://localhost:8000
npm run dev
```

App: http://localhost:5173

## API

| Method | Endpoint              | Description                                   |
|--------|-----------------------|-----------------------------------------------|
| POST   | /api/ocr/extract      | multipart upload (`file`, `remove_masthead`)  |
| GET    | /api/documents        | list extraction history (newest first)        |
| GET    | /api/documents/{id}   | fetch one result                              |
| DELETE | /api/documents/{id}   | delete a result                               |
| GET    | /api/health           | health check                                  |

## Preprocessing pipeline

`backend/app/core/preprocessing.py` — optional masthead crop (top 18%),
grayscale, 2x upscale for low-res scans, light denoising, CLAHE contrast
enhancement. Hard binarization is intentionally avoided: vision LLMs read
natural grayscale better than thresholded black-and-white.

## Notes

- Never commit `.env` — it is git-ignored. `.env.example` documents every variable.
- `detail: "high"` is set on the vision call; it costs more tokens but is
  required for dense newspaper text.
- For very long pages, split the image into halves and merge the results if
  output truncates near 4096 tokens.
