"""CRUD endpoints for stored OCR results."""
from fastapi import APIRouter, HTTPException

from app.db.database import get_db, row_to_dict
from app.models.schemas import DeleteResponse, OCRDocument, OCRDocumentList

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=OCRDocumentList)
async def list_documents(limit: int = 50, skip: int = 0):
    db = get_db()
    cursor = await db.execute("SELECT COUNT(*) FROM documents")
    total = (await cursor.fetchone())[0]
    cursor = await db.execute(
        "SELECT * FROM documents ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (min(limit, 100), skip),
    )
    docs = [row_to_dict(r) for r in await cursor.fetchall()]
    return OCRDocumentList(total=total, documents=docs)


@router.get("/{doc_id}", response_model=OCRDocument)
async def get_document(doc_id: int):
    cursor = await get_db().execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(404, "Document not found")
    return row_to_dict(row)


@router.delete("/{doc_id}", response_model=DeleteResponse)
async def delete_document(doc_id: int):
    db = get_db()
    cursor = await db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    await db.commit()
    return DeleteResponse(deleted=cursor.rowcount > 0)
