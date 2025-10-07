import io
from PIL import Image, ImageDraw




def _png_bytes_with_text(text="HELLO"):
    img = Image.new("RGB", (320, 120), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 40), text, fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf




def test_ocr_stub(client, monkeypatch):
    # 确保走 stub 分支
    monkeypatch.setenv("OCR_BACKEND", "stub")
    png = _png_bytes_with_text()
    r = client.post("/api/ocr/extract", files={"file": ("t.png", png, "image/png")})
    assert r.status_code == 200
    assert "text" in r.json()