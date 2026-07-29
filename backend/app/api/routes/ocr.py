"""OCR extraction endpoint: upload image -> preprocess -> Gemini -> store."""
from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.core.preprocessing import preprocess, to_base64_jpeg
from app.db.database import get_db, row_to_dict
from app.models.schemas import OCRDocument
from app.services.ocr_service import extract_urdu_text

router = APIRouter(prefix="/api/ocr", tags=["ocr"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp", "image/tiff"}


@router.post("/extract", response_model=OCRDocument)
async def extract(
    file: UploadFile = File(...),
    remove_masthead: bool = Form(True),
):
    settings = get_settings()

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(415, f"Unsupported file type: {file.content_type}")

    data = await file.read()
    if len(data) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_size_mb} MB limit")

    try:
        processed = preprocess(data, remove_masthead=remove_masthead)
        b64 = to_base64_jpeg(processed)
    except ValueError as e:
        raise HTTPException(422, str(e))

    try:
        text = await extract_urdu_text(b64)
    except Exception as e:
        raise HTTPException(502, f"OCR provider error: {e}")

    now = datetime.now(timezone.utc).isoformat()
    db = get_db()
    cursor = await db.execute(
        "INSERT INTO documents (filename, extracted_text, status, remove_masthead, created_at) VALUES (?, ?, ?, ?, ?)",
        (file.filename or "untitled", text, "completed", int(remove_masthead), now),
    )
    await db.commit()

    cursor2 = await db.execute("SELECT * FROM documents WHERE id = ?", (cursor.lastrowid,))
    return row_to_dict(await cursor2.fetchone())
