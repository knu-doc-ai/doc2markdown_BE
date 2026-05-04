import json
import logging
import os
import re
from pathlib import Path
import requests

from app.core.enums import MarkdownFormat
from app.core.config import settings

logger = logging.getLogger(__name__)

# 파일 서비스와 동일한 스토리지 경로 사용
STORAGE_DIR = Path("storage/documents")

def process_conversion(document_id: str, target_format: MarkdownFormat):
    doc_dir = STORAGE_DIR / document_id
    meta_path = doc_dir / "meta.json"
    pdf_path = doc_dir / "original.pdf"

    # 1. 검증 (API 레벨에서도 했지만 2차 확인)
    if not doc_dir.exists() or not meta_path.exists() or not pdf_path.exists():
        logger.error(f"Missing required files for document_id: {document_id}")
        return

    # 2. 상태를 PROCESSING으로 변경
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta_data = json.load(f)
            
        meta_data["status"] = "PROCESSING"
        
        # 이전 실패 에러가 있다면 삭제
        if "errorMessage" in meta_data:
            del meta_data["errorMessage"]
            
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to update meta.json to PROCESSING for {document_id}: {e}")
        return

    # 3. AI 서버로 변환 요청
    try:
        with open(pdf_path, "rb") as pdf_file:
            # multipart/form-data
            files_payload = {"file": ("original.pdf", pdf_file, "application/pdf")}
            data_payload = {"format": target_format.value}
            
            response = requests.post(
                settings.AI_SERVER_URL,
                files=files_payload,
                data=data_payload,
                timeout=settings.REQUEST_TIMEOUT
            )
            
        # HTTP 에러 시 예외 발생
        response.raise_for_status()
        
        # 4. AI 응답 처리
        result_data = response.json()
        markdown_content = result_data.get("markdown", "")
        images = result_data.get("images", [])

        # Markdown 텍스트 내의 로컬 경로를 웹 접속용 API 경로로 치환
        api_base = os.getenv("API_BASE_URL", "http://localhost:8000")
        markdown_content = re.sub(
            r'!\[(.*?)\]\([^)]*/([^/]+\.png)\)', 
            rf'![\1]({api_base}/documents/{document_id}/images/\2)', 
            markdown_content
        )

        # Markdown 파일 저장
        md_path = doc_dir / "original_markdown.md"
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
            
        # 이미지 저장
        if images:
            import base64
            images_dir = doc_dir / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            for idx, img in enumerate(images):
                try:
                    filename = img.get("filename", f"image_{idx}.png")
                    base64_data = img.get("data", "")
                    if base64_data:
                        img_path = images_dir / filename
                        with open(img_path, "wb") as img_file:
                            img_file.write(base64.b64decode(base64_data))
                except Exception as e:
                    logger.error(f"Failed to save image {idx}: {e}")

        # 5. 상태를 SUCCESS로 업데이트
        meta_data["status"] = "SUCCESS"
        meta_data["format"] = target_format.value
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, ensure_ascii=False, indent=2)
            
    except requests.exceptions.Timeout:
        _handle_conversion_failure(meta_path, meta_data, "Timeout while connecting to AI server")
    except requests.exceptions.RequestException as e:
        _handle_conversion_failure(meta_path, meta_data, f"AI server request failed: {str(e)}")
    except Exception as e:
        _handle_conversion_failure(meta_path, meta_data, f"Internal error during conversion: {str(e)}")

def _handle_conversion_failure(meta_path: Path, meta_data: dict, error_message: str):
    logger.error(f"Conversion failed: {error_message}")
    meta_data["status"] = "FAILED"
    meta_data["errorMessage"] = error_message
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to write error state to meta.json: {e}")
