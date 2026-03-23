from fastapi import APIRouter, File, UploadFile, HTTPException, status
from app.schemas.document_schema import DocumentUploadResponse
from app.services.file_service import save_uploaded_file

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
