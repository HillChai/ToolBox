from __future__ import annotations
from typing import Optional
from functools import lru_cache
from fastapi import UploadFile
from pathlib import Path
import tempfile


from app.models.schemas import AsrResult
from app.core.config import settings




@lru_cache(maxsize=4)
def _get_whisper_model(size: str):
    from faster_whisper import WhisperModel
    # CPU 默认 int8 更快；有 GPU 可传 compute_type="float16" 并 device="cuda"
    return WhisperModel(size, device="cpu", compute_type="int8")




def _ensure_local_path(path: Optional[str], file: Optional[UploadFile]) -> str:
    if path:
        return path
    assert file is not None
    suffix = Path(file.filename or "audio").suffix or ".wav"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(file.file.read())
    tmp.flush(); tmp.close()
    return tmp.name




async def transcribe(path: Optional[str] = None, file: Optional[UploadFile] = None, model_size: str = "base", language: Optional[str] = None) -> AsrResult:
    if settings.ASR_BACKEND != "faster_whisper":
        return AsrResult(text="(stub) transcription", language=language)

    local = _ensure_local_path(path, file)

    model = _get_whisper_model(model_size)
    segments, info = model.transcribe(local, language=language)
    text = " ".join([seg.text.strip() for seg in segments])
    return AsrResult(text=text.strip(), language=info.language, duration_sec=info.duration)