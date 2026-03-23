import os
import json
import uuid
import time
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException

STORAGE_DIR = Path("storage/documents")

def generate_document_id() -> str:
    timestamp = int(time.time())
    random_str = uuid.uuid4().hex[:6]
    return f"doc_{timestamp}_{random_str}"

def save_uploaded_file(file: UploadFile) -> str:
    try:
        document_id = generate_document_id()
        doc_dir = STORAGE_DIR / document_id
        
        # storage/documents/{documentId} 디렉토리 생성
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        # original.pdf 저장
        pdf_path = doc_dir / "original.pdf"
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # meta.json 저장
        meta_data = {
            "documentId": document_id,
            "fileName": file.filename,
            "status": "UPLOADED",
            "format": None
        }
        
        meta_path = doc_dir / "meta.json"
        with open(meta_path, "w", encoding="utf-8") as meta_file:
            json.dump(meta_data, meta_file, ensure_ascii=False, indent=2)
            
        return document_id
    except Exception as e:
        # 실패 시 디렉토리가 생성되었다면 롤백
        if 'doc_dir' in locals() and doc_dir.exists():
            shutil.rmtree(doc_dir)
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
