from __future__ import annotations
from typing import Optional, List
from functools import lru_cache


import torch
from torchvision import models, transforms
from torch.nn import functional as F


from fastapi import UploadFile
from app.utils.image_io import load_pil_image
from app.models.schemas import VisionResult, TopK
from app.core.config import settings




@lru_cache(maxsize=1)
def _get_model_and_tfms():
    weights = models.ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)
    model.eval()
    tfm = weights.transforms()
    categories: List[str] = weights.meta["categories"]
    return model, tfm, categories




def _infer_species(label: str) -> str:
    # ImageNet 猫类标签包含 'cat'；狗是具体品种名（大多不含 'dog'）。这里做简化判断：
    if "cat" in label.lower():
        return "cat"
    # 若不是猫，默认视为狗（你的使用场景限定在猫/狗）。
    return "dog"




async def classify_cat_dog(path: Optional[str] = None, file: Optional[UploadFile] = None) -> VisionResult:
    if settings.VISION_BACKEND != "torchvision":
        return VisionResult(species="unknown", breed="unknown", top5=[])

    return VisionResult(species=species, breed=breed, top5=top5)