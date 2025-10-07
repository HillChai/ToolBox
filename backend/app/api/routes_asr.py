from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services.asr import transcribe
from app.models.schemas import AsrResult


router = APIRouter(prefix="/asr", tags=["asr"])


@router.post("/transcribe", response_model=AsrResult)
async def asr_transcribe(
file: UploadFile | None = File(default=None),
path: str | None = Query(default=None, description="Server-side stored audio path"),
model_size: str = Query(default="base", description="faster-whisper model size: tiny/base/small/medium/large-v3"),
language: str | None = Query(default=None, description="Force language code like 'zh' or 'en' (optional)"),
):
    if file is None and not path:
        raise HTTPException(status_code=400, detail="Provide either an uploaded audio or a server path")
    return await transcribe(file=file, path=path, model_size=model_size, language=language)