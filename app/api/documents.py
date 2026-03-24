from fastapi import APIRouter, File, UploadFile, HTTPException, status, BackgroundTasks
from pathlib import Path

from app.schemas.document_schema import DocumentUploadResponse, ConvertRequest, ConvertResponse
from app.services.file_service import save_uploaded_file, STORAGE_DIR
from app.services.convert_service import process_conversion

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    # 1. 파일 존재 여부 확인 (UploadFile이 None인 경우는 FastAPI가 기본으로 422 언프로세서블 엔티티 에러를 내지만, 직접 처리할 수도 있음)
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="File is missing")
        
    # 2. 확장자 및 Content-Type 검증
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are allowed")
        
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid content type. Must be application/pdf")

    # 3. 파일 저장 및 메타데이터 생성 (Service 로직 호출)
    try:
        document_id = save_uploaded_file(file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file")

    # 4. 성공 응답 반환
    return DocumentUploadResponse(
        documentId=document_id,
        fileName=file.filename,
        status="UPLOADED"
    )

@router.post("/{document_id}/convert", response_model=ConvertResponse, status_code=status.HTTP_202_ACCEPTED)
async def convert_document(document_id: str, request: ConvertRequest, background_tasks: BackgroundTasks):
    doc_dir = STORAGE_DIR / document_id
    pdf_path = doc_dir / "original.pdf"
    meta_path = doc_dir / "meta.json"

    # 1. 문서 및 파일 존재 여부 검증
    if not doc_dir.exists() or not pdf_path.exists() or not meta_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # 2. 백그라운드 변환 작업 큐잉
    background_tasks.add_task(process_conversion, document_id, request.format)

    # 3. 비동기 처리 응답 (PROCESSING & 202 Accepted) 반환
    return ConvertResponse(documentId=document_id, status="PROCESSING")
