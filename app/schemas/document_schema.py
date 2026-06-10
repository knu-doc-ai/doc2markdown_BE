from typing import Optional
from pydantic import BaseModel
from app.core.enums import MarkdownFormat

class DocumentUploadResponse(BaseModel):
    documentId: str
    fileName: str
    status: str

class ConvertRequest(BaseModel):
    format: MarkdownFormat

class ConvertResponse(BaseModel):
    documentId: str
    status: str

class DocumentStatusResponse(BaseModel):
    documentId: str
    fileName: str
    status: str  # UPLOADED | PROCESSING | SUCCESS | FAILED
    format: Optional[str] = None
    errorMessage: Optional[str] = None

class ResultResponse(BaseModel):
    documentId: str
    status: str
    format: Optional[str] = None
    markdown: str
    images: list[str]

class MarkdownSaveRequest(BaseModel):
    markdown: str

class MarkdownSaveResponse(BaseModel):
    documentId: str
    status: str
