import os

class Settings:
    # 환경변수에서 AI 서버 주소를 가져오며, 없을 경우 기본값 세팅
    AI_SERVER_URL: str = os.getenv("AI_SERVER_URL", "http://localhost:8001/ai/convert")
    
    # AI 요청 Timeout (기본 5분 = 300초 설정)
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "300"))

settings = Settings()
