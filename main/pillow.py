from PIL import Image
import io, hashlib, time
from pathlib import Path
from typing import List

from .song import Song
from .song_subclasses import MP3Song

SIZES = [(512,512), (256,256), (128,128), (64,64)]

def _base_dir() -> Path:
    return Path(__file__).resolve().parent.parent

def _center_crop_to_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    m = min(w, h)
    left = (w - m) // 2
    top = (h - m) // 2
    return img.crop((left, top, left + m, top + m))

def resize_image_bytes(input_bytes, sizes: List[tuple[int, int]]) -> dict[int, bytes]:
    # Load bytes into PIL
    img = Image.open(io.BytesIO(input_bytes))
    img = _center_crop_to_square(img)
    image_dict = {}
    for size in sizes:
        # Resize image
        resized_img = img.resize(size)
        # Save back to bytes
        output = io.BytesIO()
        resized_img.save(output, format="JPEG")
        image_dict[size[0]] = output.getvalue()
        img = resized_img


    return image_dict


def cache_image_bytes(data: bytes | None, cache_dir: Path, sizes : List[tuple[int, int]], ext : str = ".jpg") -> Path | None:
    if not data:
        return None

    digest = hashlib.sha256(data).hexdigest()
    path = cache_dir / digest[:2] / digest
    if not path.exists():
        image_dict = resize_image_bytes(data,sizes)

        for size, bytes in image_dict.items():
            path = cache_dir / digest[:2] / digest / f"{size}{ext}"
            print(str(path))
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                f.write(bytes)

    return path


def enumerate_audio_files() -> list[Path]:
    base_dir = Path(__file__).resolve().parent.parent
    music_folder = base_dir / "music"
    files : list[Path] = []
    for pattern in ("*.mp3", "*.m4a", "*.flac"):
        files.extend(music_folder.rglob(pattern))
    return files


song_list = enumerate_audio_files()
art_dir = _base_dir() / "mock_cache" / "album_art"

start = time.time()
for idx in song_list:
    song = MP3Song(idx)
    art_bytes = song.get_art()
    cache_image_bytes(art_bytes, art_dir, ext = ".jpg", sizes = SIZES)
finish = time.time()
print(f"Total time: {finish-start}")