# GenAI Agent 실행 가이드 (개발용)

## 전체 구조 요약
- **백엔드 (FastAPI)** → `localhost:8000`
- **프론트엔드 (Flask)** → `localhost:5000/prototype`

---

## 터미널 1: FastAPI 백엔드 실행
```bash
cd genai-dev-pipeline-template/genai-dev-pipeline
uvicorn agent.main:app --reload --port 8000
```

> Swagger 확인: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 터미널 2: Flask 프론트엔드 실행
```bash
cd genai-dev-pipeline-template/genai-dev-pipeline/frontend/prototype
python app.py
```

> 테스트 화면 접속: [http://localhost:5000/prototype](http://localhost:5000/prototype)

---

## Tips
- `.env` 또는 `settings.py`에서 `IS_MOCK_MODE=True`일 때는 Mock 모드로 작동함
- 백엔드 서버가 꺼져 있으면 프론트에서 "연결 실패" 오류 발생함
- 두 서버는 반드시 **각기 다른 터미널에서 동시에 실행**해야 함
