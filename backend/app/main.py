"""FastAPI application entrypoint."""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import documents, ocr
from app.config import get_settings
from app.db import mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.connect()
    yield
    await mongodb.disconnect()


app = FastAPI(
    title="Urdu Newspaper OCR API",
    description="Extract Urdu Nastaliq text from newspaper scans using Gemini",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router)
app.include_router(documents.router)


@app.get("/api/health", tags=["health"])
async def health():
    return {"status": "ok"}


frontend_dist = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
