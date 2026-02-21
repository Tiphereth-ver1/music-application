from PIL import Image
import io, hashlib, time
from pathlib import Path
from typing import List
from PySide6.QtGui import QPixmap

from .song import Song
from .song_subclasses import MP3Song

SIZES = [(512,512), (256,256), (192,192), (128,128), (64,64)]

def _center_crop_to_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    m = min(w, h)
    left = (w - m) // 2
    top = (h - m) // 2
    return img.crop((left, top, left + m, top + m))

def _resize_image_bytes(input_bytes, sizes: List[tuple[int, int]] = SIZES) -> dict[int, bytes]:
    img = Image.open(io.BytesIO(input_bytes))
    img = _center_crop_to_square(img)

    # JPEG can't store alpha; flatten/convert
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        # Flatten alpha onto black (or pick another background)
        bg = Image.new("RGB", img.size, (0, 0, 0))
        img = Image.alpha_composite(bg.convert("RGBA"), img.convert("RGBA")).convert("RGB")
    else:
        img = img.convert("RGB")

    image_dict = {}
    for size in sizes:
        resized_img = img.resize(size, Image.Resampling.LANCZOS)
        output = io.BytesIO()
        resized_img.save(output, format="JPEG", quality=85, optimize=True)
        image_dict[size[0]] = output.getvalue()

    return image_dict

def _base_dir() -> Path:
    return Path(__file__).resolve().parent.parent

class ArtCache:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self._pixmap_cache: dict[tuple[str, int], QPixmap] = {}
    
    def update_cache_dir(self, cache_dir):
        self.cache_dir = cache_dir
        self._pixmap_cache.clear()

    def get_hex_cache(self, data: bytes | None) -> str | None:
        if not data:
            return None
        return hashlib.sha256(data).hexdigest()

    def cache_image_bytes(self, data: bytes | None, ext=".jpg", sizes=SIZES) -> Path | None:
        if not data:
            return None

        digest = hashlib.sha256(data).hexdigest()
        dir_path = self.cache_dir / digest[:2] / digest

        if not dir_path.exists():
            image_dict = _resize_image_bytes(data)

            for size, img_bytes in image_dict.items():
                file_path = dir_path / f"{size}{ext}"
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(img_bytes)

        return dir_path

    def get_image_cache(self, hex: str, size : int, ext : str = ".jpg"):
        if not hex:
            return None
        path = self.cache_dir / hex[:2] / hex / f"{size}{ext}"
        if path.exists():
            return path
        return None

    def get_pixmap(self, hex: str, size: int) -> QPixmap | None:
        key = (hex, size)

        if key in self._pixmap_cache:
            return self._pixmap_cache[key]

        path = self.get_image_cache(hex, size)
        if not path:
            return None

        pix = QPixmap(str(path))
        if pix.isNull():
            return None

        self._pixmap_cache[key] = pix
        return pix