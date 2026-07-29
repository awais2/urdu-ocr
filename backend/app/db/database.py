"""Async SQLite database management."""
import os
from datetime import datetime

import aiosqlite

from app.config import get_settings

_db: aiosqlite.Connection | None = None


async def connect() -> None:
    global _db
    settings = get_settings()
    os.makedirs(os.path.dirname(settings.database_path) or ".", exist_ok=True)
    _db = await aiosqlite.connect(settings.database_path)
    _db.row_factory = aiosqlite.Row
    await _db.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'completed',
            remove_masthead INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_documents_created_at
            ON documents(created_at DESC);
    """)
    await _db.commit()


async def disconnect() -> None:
    global _db
    if _db is not None:
        await _db.close()
        _db = None


def get_db() -> aiosqlite.Connection:
    if _db is None:
        raise RuntimeError("Database not initialized")
    return _db


def row_to_dict(row: aiosqlite.Row) -> dict:
    return dict(
        id=str(row["id"]),
        filename=row["filename"],
        extracted_text=row["extracted_text"],
        status=row["status"],
        remove_masthead=bool(row["remove_masthead"]),
        created_at=datetime.fromisoformat(row["created_at"]),
    )
