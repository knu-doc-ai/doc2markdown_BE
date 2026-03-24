import subprocess
import time
import requests
import json
import io
import sys
from pathlib import Path

def run_test():
    print("🚀 테스트용 FastAPI 서버를 시작합니다...")
    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8008"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # 서버가 뜰 때까지 대기
    
    try:
        base_url = "http://localhost:8008"
        
        print("\n[1] 더미 PDF 파일 업로드 중...")
        dummy_pdf = io.BytesIO(b"%PDF-1.4 dummy test pdf content")
        res1 = requests.post(f"{base_url}/documents/upload", files={"file": ("test.pdf", dummy_pdf, "application/pdf")})
        res1.raise_for_status()
        doc_id = res1.json()["documentId"]
        print(f"✅ 업로드 성공! documentId: {doc_id}")
        
        print(f"\n[2] Markdown 변환 요청 (format: gfm)...")
        res2 = requests.post(f"{base_url}/documents/{doc_id}/convert", json={"format": "gfm"})
        res2.raise_for_status()
        print(f"✅ 변환 요청 수락됨! (202 Accepted) | 응답값: {res2.json()}")
        
        print("\n[3] 백그라운드 태스크 처리 결과 확인 (meta.json 읽기)...")
        meta_path = Path(f"storage/documents/{doc_id}/meta.json")
        for _ in range(10):
            time.sleep(0.5)
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if meta.get("status") in ["SUCCESS", "FAILED"]:
                print(f"✅ 백그라운드 처리 완료! 최종 상태: {meta.get('status')}")
                if "errorMessage" in meta:
                     print(f"   👉 메타데이터 내 Error 메세지: {meta.get('errorMessage')}")
                break
        else:
            print("⏳ 백그라운드 작업이 너무 오래 걸립니다.")
            
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
    finally:
        print("\n🛑 테스트 서버를 종료합니다...")
        server.terminate()
        server.wait()

if __name__ == "__main__":
    run_test()
