from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    documentId: str
    fileName: str
    status: str
