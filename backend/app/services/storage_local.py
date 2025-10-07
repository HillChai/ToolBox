from pathlib import Path
from typing import BinaryIO
from app.core.config import settings

class LocalObjectStorage:
    def __init__(self, root: Path | None = None):
        self.root = (root or (settings.DATA_DIR / "objects")).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, stream: BinaryIO) -> Path:
        path = (self.root / key).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as w:
            stream.seek(0)
            while True:
                b = stream.read(1024 * 1024)
                if not b:
                    break
                w.write(b)
        return path

    def get_path(self, key: str) -> Path:
        return (self.root / key).resolve()