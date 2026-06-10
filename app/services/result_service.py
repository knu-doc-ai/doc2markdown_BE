import json
from pathlib import Path
from fastapi import HTTPException, status

from app.services.file_service import STORAGE_DIR


def get_document_result(document_id: str) -> dict:
    """변환 결과를 읽어 딕셔너리로 반환한다."""
    doc_dir: Path = STORAGE_DIR / document_id

    # 1. documentId 폴더 존재 확인
    if not doc_dir.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # 2. meta.json 존재 확인 및 읽기
    meta_path = doc_dir / "meta.json"
    if not meta_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="meta.json not found"
        )

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read meta.json"
        )

    # 3. original_markdown.md 존재 확인 및 읽기
    markdown_path = doc_dir / "original_markdown.md"
    if not markdown_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Markdown result not found"
        )

    try:
        with open(markdown_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read markdown file"
        )

    # 4. images/ 폴더 내 파일명 목록 수집
    images_dir = doc_dir / "images"
    images: list[str] = []
    if images_dir.exists() and images_dir.is_dir():
        images = [f.name for f in sorted(images_dir.iterdir()) if f.is_file()]

    return {
        "documentId": meta.get("documentId", document_id),
        "status": meta.get("status", ""),
        "format": meta.get("format"),
        "markdown": markdown_content,
        "images": images,
    }
