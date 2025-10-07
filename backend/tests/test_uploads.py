import io


def test_upload_accepts_any_file(client):
    data = io.BytesIO(b"dummy-data")
    r = client.post("/api/files/upload", files={"file": ("a.bin", data, "application/octet-stream")})
    js = r.json()
    assert r.status_code == 200
    assert "path" in js and js["size_bytes"] == 10