from __future__ import annotations
from typing import Optional
from fastapi import UploadFile
from PIL import Image
from io import BytesIO




def load_pil_image(path: Optional[str] = None, file: Optional[UploadFile] = None) -> Image.Image:
    if path:
        return Image.open(path).convert("RGB")
    assert file is not None
    data = file.file.read()
    return Image.open(BytesIO(data)).convert("RGB")