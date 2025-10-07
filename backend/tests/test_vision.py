import io
import pytest
from PIL import Image


@pytest.mark.slow
def test_vision_real_if_enabled(client, monkeypatch):
    # 仅当你想真正跑 torchvision/torch 时再启用
    monkeypatch.setenv("VISION_BACKEND", "torchvision")
    # 生成纯色图片（不一定分类准，仅验证端到端流程）
    img = Image.new("RGB", (224, 224), color=(200, 180, 160))
    buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    r = client.post("/api/vision/cat-dog", files={"file": ("x.png", buf, "image/png")})
    assert r.status_code == 200
    js = r.json()
    assert {"species", "breed", "top5"}.issubset(js.keys())