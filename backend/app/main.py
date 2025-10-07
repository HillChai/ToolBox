# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, Base
import app.models  # noqa: F401  确保模型被导入
from app.api import routes_uploads, routes_ocr, routes_asr, routes_vision, routes_health

app = FastAPI(title="AI Backend")

# CORS（按需）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# 开发阶段自动建表（生产建议 Alembic）
Base.metadata.create_all(bind=engine)

# 路由
app.include_router(routes_health.router, prefix="/api")
app.include_router(routes_uploads.router, prefix="/api")
app.include_router(routes_ocr.router, prefix="/api")
app.include_router(routes_asr.router, prefix="/api")
app.include_router(routes_vision.router, prefix="/api")
