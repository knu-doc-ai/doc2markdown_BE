import json
from pathlib import Path
from fastapi import HTTPException, status

from app.services.file_service import STORAGE_DIR

def save_markdown(document_id: str, markdown: str) -> None:
    """사용자가 수정한 Markdown을 저장하고 meta.json을 업데이트한다."""
    doc_dir: Path = STORAGE_DIR / document_id

    # 1. documentId 폴더 존재 확인
    if not doc_dir.exists() or not doc_dir.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # meta.json 존재 여부 확인
    meta_path = doc_dir / "meta.json"
    if not meta_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="meta.json not found"
        )

    try:
        # 2. edited_markdown.md에 내용 저장 (빈 문자열도 허용됨)
        edited_markdown_path = doc_dir / "edited_markdown.md"
        with open(edited_markdown_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        # 3. meta.json 읽기 및 업데이트
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        # edited 필드를 True로 추가하거나 업데이트
        meta["edited"] = True

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save markdown file or update document metadata"
        )
