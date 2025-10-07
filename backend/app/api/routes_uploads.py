# app/api/routes_uploads.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Upload, AuditLog
from app.models.schemas import FileCreate, FileOut, PageResult
from app.utils.crypto import sha256_stream
from app.services.storage_local import LocalObjectStorage

from pathlib import Path

router = APIRouter(prefix="/uploads", tags=["uploads"])
storage = LocalObjectStorage()

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=FileOut)
def upload_file(request: Request, file: UploadFile = File(...)):
    # 读入内存/临时文件计算哈希
    import io
    buf = io.BytesIO(file.file.read())
    buf.seek(0)
    digest = sha256_stream(buf)
    buf.seek(0)

    # 生成对象存储 key：按哈希分片，保留原始扩展名
    ext = Path(file.filename).suffix.lower()
    key = f"{digest[:2]}/{digest[2:4]}/{digest}{ext or ''}"

    # 写入本地对象存储
    storage.put(key, buf)

    # 记录到数据库
    with SessionLocal() as db:
        row = Upload(
            user_id=None,
            original_filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            size_bytes=len(buf.getbuffer()),
            hash_sha256=digest,
            storage_key=key,
        )
        db.add(row)
        db.flush()
        db.refresh(row)

        # 审计
        db.add(AuditLog(
            action="UPLOAD",
            subject_id=row.id,
            ip=request.client.host if request.client else None,
            ua=request.headers.get("user-agent"),
            extra_json={"filename": file.filename}
        ))
        db.commit()

        return FileOut(
            id=row.id,
            filename=row.original_filename,
            content_type=row.content_type,
            size_bytes=row.size_bytes,
            download_url=f"/api/uploads/{row.id}/download"
        )

@router.get("", response_model=PageResult)
def list_uploads(page: int = 1, size: int = 20):
    page = max(page, 1)
    size = max(min(size, 200), 1)
    with SessionLocal() as db:
        total = db.scalar(select(func.count()).select_from(Upload)) or 0
        rows = db.execute(
            select(Upload).order_by(Upload.created_at.desc()).offset((page-1)*size).limit(size)
        ).scalars().all()
        items = [
            FileOut(
                id=r.id, filename=r.original_filename, content_type=r.content_type,
                size_bytes=r.size_bytes, download_url=f"/api/uploads/{r.id}/download"
            ) for r in rows
        ]
        return PageResult(items=items, total=total, page=page, size=size)

@router.get("/{upload_id}/download")
def download_upload(upload_id: str, request: Request):
    with SessionLocal() as db:
        row = db.get(Upload, upload_id)
        if not row:
            raise HTTPException(status_code=404, detail="File not found")
        path = storage.get_path(row.storage_key)
        if not path.exists():
            raise HTTPException(status_code=410, detail="File missing in object store")

        # 审计
        db.add(AuditLog(
            action="DOWNLOAD",
            subject_id=row.id,
            ip=request.client.host if request.client else None,
            ua=request.headers.get("user-agent"),
        ))
        db.commit()

        return FileResponse(
            path=path,
            media_type=row.content_type,
            filename=row.original_filename
        )
