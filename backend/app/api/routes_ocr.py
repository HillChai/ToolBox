from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services.ocr import extract_text
from app.models.schemas import OcrResult


router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post("/extract", response_model=OcrResult)
async def ocr_extract(
    file: UploadFile | None = File(default=None),
    path: str | None = Query(default=None, description="Server-stored image path"),
    lang: str = Query(default="eng", description="tesseract lang, e.g. eng, chi_sim, eng+chi_sim"),
    ):
    if file is None and not path:
        raise HTTPException(status_code=400, detail="Provide either an uploaded image or a server path")
    return await extract_text(file=file, path=path, lang=lang)