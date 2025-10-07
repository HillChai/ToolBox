from __future__ import annotations
from typing import Optional
import re
import statistics
from fastapi import UploadFile
from PIL import Image
import pytesseract
from app.utils.image_io import load_pil_image
from app.models.schemas import OcrResult
from app.core.config import settings




async def extract_text(path: Optional[str] = None, file: Optional[UploadFile] = None, lang: str = "eng") -> OcrResult:
    if settings.OCR_BACKEND != "tesseract":
        # 简单兜底
        return OcrResult(text="(stub) ocr result", lang=lang)


img: Image.Image = load_pil_image(path=path, file=file)
# 常用配置：oem 3: default LSTM; psm 6: assume a block of text
config = "--oem 3 --psm 6"
text = pytesseract.image_to_string(img, lang=lang, config=config)


# 计算平均置信度（可选）
try:
    data = pytesseract.image_to_data(img, lang=lang, config=config, output_type=pytesseract.Output.DICT)
    confs = [float(c) for c in data.get("conf", []) if c not in ("-1", "-1.0")]
    avg_conf = round(statistics.fmean(confs), 2) if confs else None
except Exception:
    avg_conf = None
