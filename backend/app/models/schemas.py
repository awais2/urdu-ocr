"""API request/response schemas."""
from datetime import datetime

from pydantic import BaseModel, Field


class OCRDocument(BaseModel):
    id: str = Field(..., description="Document id")
    filename: str
    extracted_text: str
    status: str = "completed"
    remove_masthead: bool = True
    created_at: datetime


class OCRDocumentList(BaseModel):
    total: int
    documents: list[OCRDocument]


class DeleteResponse(BaseModel):
    deleted: bool
