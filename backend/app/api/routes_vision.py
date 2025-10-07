from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services.vision import classify_cat_dog
from app.models.schemas import VisionResult


router = APIRouter(prefix="/vision", tags=["vision"])


@router.post("/cat-dog", response_model=VisionResult)
async def cat_dog(
    file: UploadFile | None = File(default=None),
    path: str | None = Query(default=None, description="Server-stored image path"),
):
    if file is None and not path:
        raise HTTPException(status_code=400, detail="Provide either an uploaded image or a server path")
    return await classify_cat_dog(file=file, path=path)