import io
import zipfile
from pathlib import Path
from fastapi import HTTPException, status

from app.services.file_service import STORAGE_DIR

def get_final_markdown_path(document_id: str) -> Path | None:
    """반환할 최종 마크다운 파일의 경로를 결정한다."""
    doc_dir: Path = STORAGE_DIR / document_id
    edited_path = doc_dir / "edited_markdown.md"
    original_path = doc_dir / "original_markdown.md"
    
    # 수정된 파일이 있으면 1순위
    if edited_path.exists() and edited_path.is_file():
        return edited_path
    
    # 수정본이 없으면 원본 반환
    if original_path.exists() and original_path.is_file():
        return original_path
        
    return None

def create_download_zip_stream(document_id: str) -> io.BytesIO:
    """최종 마크다운 파일과 이미지들을 압축하여 BytesIO 스트림으로 반환한다."""
    doc_dir: Path = STORAGE_DIR / document_id

    # 1. documentId 폴더 존재 확인
    if not doc_dir.exists() or not doc_dir.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
        
    # 2. 다운로드할 최종 마크다운 파일 결정
    markdown_path = get_final_markdown_path(document_id)
    if not markdown_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Final markdown not found"
        )
        
    # 3. zip 생성 및 BytesIO 스트림 반환을 위한 준비
    memory_file = io.BytesIO()
    
    try:
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 마크다운 파일을 압축 파일 내 'document.md'로 고정하여 작성
            zf.write(markdown_path, arcname="document.md")
            
            # images/ 폴더 확인 및 내부 파일들 추가
            images_dir = doc_dir / "images"
            if images_dir.exists() and images_dir.is_dir():
                for file_path in images_dir.iterdir():
                    # 이미지 폴더 내부의 '파일'만 zip에 포함하도록 조건 추가
                    if file_path.is_file():
                        zf.write(file_path, arcname=f"images/{file_path.name}")
                        
        # 4. 스트림의 포인터를 처음으로 이동
        memory_file.seek(0)
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create download zip file"
        )
        
    return memory_file
