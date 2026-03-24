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
