import os

class Settings:
    # 환경변수에서 AI 서버 주소를 가져오며, 없을 경우 기본값 세팅
    AI_SERVER_URL: str = os.getenv("AI_SERVER_URL", "http://localhost:8001/ai/convert")
    
    # AI 요청 Timeout (기본 20분 = 1200초 설정: 로컬 CPU 환경에서의 구동 목적)
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "1200"))

settings = Settings()
