import os
import pytest
from fastapi.testclient import TestClient


# 默认将后端切换到 stub，避免本机无 Tesseract/Whisper 时测试失败
os.environ.setdefault("OCR_BACKEND", "stub")
os.environ.setdefault("ASR_BACKEND", "stub")
os.environ.setdefault("VISION_BACKEND", "stub")
os.environ.setdefault("MAX_CONCURRENCY", "1")


from app.main import app # 在设置 env 之后再导入 app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)