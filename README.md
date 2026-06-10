

---

# 📄 [LG전자 산학협력] 비전 AI 기반의 레이아웃 보존형 문서-Markdown 자동 변환 에이전트 (Backend)

## 📌 프로젝트 소개

본 레포지토리는 '레이아웃 보존형 문서-Markdown 자동 변환 AI 에이전트'의 핵심 비즈니스 로직과 AI 변환 파이프라인을 구동하는 **백엔드(BE) API 서버**입니다.
FastAPI 프레임워크를 기반으로 구축되었으며, 사용자가 업로드한 PDF/이미지 문서의 시각적 구조를 분석하고 멀티모달 및 로컬/원격 LLM 에이전트(Ollama, OpenAI 등)를 활용하여 원본 레이아웃을 90% 이상 보존하는 고품질 Markdown 정제 및 조립 기능을 수행합니다.

## 🛠 기술 스택 (Tech Stack)

* **Framework:** FastAPI
* **ASGI Server:** Uvicorn
* **Language:** Python 3.10+
* **Data Validation:** Pydantic
* **AI Core & Agent Orchestration:** PyTorch, OpenAI API, Anthropic API, Ollama (GGUF Local Integration)
* **Environment Management:** Python-dotenv, Pydantic-settings

## 📂 디렉토리 구조 (Directory Structure)

프로젝트는 FastAPI의 모범 사례에 맞추어 관심사 분리(Separation of Concerns) 아키텍처에 따라 모듈화되어 있습니다.

```text
doc2markdown_BE/
│
├── app/                        # 💻 메인 애플리케이션 패키지
│   ├── main.py                 # FastAPI 인스턴스 생성, 미들웨어(CORS) 및 루트 설정
│   │
│   ├── api/                    # 🌐 API 라우터 레이어 (엔드포인트)
│   │   ├── router.py           # 서비스 내 하위 라우터들을 통합하는 루트 라우터
│   │   └── documents.py        # 문서 업로드, 변환 진행률 조회, 결과 수정 및 다운로드 API
│   │
│   ├── core/                   # ⚙️ 애플리케이션 전역 설정 및 상수
│   │   ├── config.py           # 전역 환경 변수 관리 (.env 파싱 및 Pydantic Settings 확장)
│   │   └── enums.py            # 변환 파이프라인 단계 및 상태(Status) 정의 공통 Enum
│   │
│   ├── schemas/                # 📊 데이터 유효성 검증 및 직렬화 레이어 (DTO)
│   │   └── document_schema.py  # 문서 요청/응답 데이터 검증을 위한 Pydantic 모델
│   │
│   └── services/               # ⚙️ 핵심 비즈니스 로직 및 AI 에이전트 서비스 레이어
│       ├── file_service.py     # 원본 PDF/이미지 및 임시 파일 저장, 경로 검증 및 관리
│       ├── convert_service.py  # 시각 구조 분석 모듈 및 LLM 보강 파이프라인 오케스트레이터
│       ├── markdown_service.py # 정제된 중간 표현(IR) 데이터를 최종 Markdown 스펙으로 파싱 및 조립
│       ├── download_service.py # 변환 완료된 Markdown 파일 및 이미지 에셋의 ZIP 압축 처리
│       └── result_service.py   # 사용자의 수동 보정 내용 반영 및 변환 이력 데이터 상태 관리
│
├── .vscode/                    # VS Code 작업 영역 개인 설정
├── .gitignore                  # Git 추적 제외 목록
├── requirements.txt            # 의존성 Python 패키지 목록
├── test_api.py                 # 단위 API 및 개별 엔드포인트 동작 검증 스크립트
└── test_api_flow.py            # 파일 업로드부터 최종 변환 완료까지의 전체 파이프라인 E2E 테스트 스크립트

```

## 🚀 시작하기 (Getting Started)

### 1. 가상환경 생성 및 패키지 설치

안정적인 패키지 의존성 관리를 위해 `conda` 또는 `venv`를 활용한 독립적인 가상환경 사용을 권장합니다.

```bash
# 1. 가상환경 생성 및 활성화 (예: conda)
conda create -n lg_agent_be python=3.10
conda activate lg_agent_be

# 2. 필수 패키지 일괄 설치
pip install -r requirements.txt

# 3. 비전/레이아웃 분석 엔진용 GPU 구동 환경 설정 (CUDA 11.8 기준 예시)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

```

### 2. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 프레임워크 동작 설정 및 외부 AI API 인증키, 로컬 Ollama 환경 변수 설정을 마칩니다.

```env
# API 서버 구동 환경 설정
ENV=development
API_V1_STR=/api
PROJECT_NAME="Doc2Markdown-AI-Agent-Backend"

# 외부 LLM API 키 설정 (필요 시)
OPENAI_API_KEY="your-openai-api-key"
ANTHROPIC_API_KEY="your-anthropic-api-key"

# 로컬 임베디드 / 노트북 구동 환경용 Ollama 설정
LOCAL_LLM_BASE_URL="http://127.0.0.1:11434/v1"
LOCAL_LLM_API_KEY="ollama"
LOCAL_LLM_SEMANTIC_MODEL_ID="hf.co/ggml-org/Qwen3-0.6B-GGUF:Q4_0"
LOCAL_LLM_CONTENT_MODEL_ID="hf.co/ggml-org/Qwen3-0.6B-GGUF:Q4_0"

# 파이프라인 배치 스펙 제어
LLM_SEMANTIC_BATCH_SIZE="32"
LLM_CONTENT_BATCH_SIZE="2"
LLM_REQUEST_TIMEOUT_SECONDS="60"

```

### 3. API 개발 서버 실행

`uvicorn`을 사용하여 로컬 개발 서버를 구동합니다. `--reload` 옵션을 부여하면 코드가 수정될 때마다 서버가 자동으로 재시작됩니다.

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

```

서버가 정상적으로 백그라운드에서 실행되면 `http://127.0.0.1:8000/docs` (Swagger UI)에 접속하여 백엔드가 제공하는 모든 엔드포인트를 시각적으로 확인하고 직접 테스트해 볼 수 있습니다.

## 🧪 테스트 가이드 (Testing)

애플리케이션의 엔드포인트 신뢰성과 AI 파이프라인의 안전성을 검증하기 위한 테스트 스크립트를 제공합니다.

* **단일 기능/API 테스트:**
```bash
python test_api.py

```


* **전체 시나리오 E2E 흐름 테스트 (업로드 ➡️ 시각 구조 분석 ➡️ IR 추출 ➡️ 에이전트 보강 ➡️ MD 조립):**
```bash
python test_api_flow.py

```
