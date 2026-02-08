from PySide6.QtCore import QUrl, Signal, QObject
from typing import Any
from pathlib import Path
from abc import ABC, abstractmethod
import re
import unicodedata


TAG_MAP = {
    "title": None,
    "artist": None,
    "album": None,
    "album_artist" : None,
    "track": None,
    "track_total": None,
    "genre": None,
    "year": None,
}

WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

ILLEGAL_CHARS = r'<>:"/\\|?*\x00-\x1F'

def sanitize_filename(
    name: str,
    replacement: str = "_",
    max_length: int = 255
) -> str:
    # Normalize Unicode (é vs e + ´ etc.)
    name = unicodedata.normalize("NFKC", name)

    # Replace illegal characters
    name = re.sub(f"[{ILLEGAL_CHARS}]", replacement, name)

    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()

    # Remove trailing dots/spaces (Windows rule)
    name = name.rstrip(". ")

    # Guard reserved device names
    if name.upper() in WINDOWS_RESERVED:
        name = f"_{name}"

    # Final length clamp (leave room for extension)
    return name[:max_length]


class Song(QObject):
    changed = Signal()

    def __init__(self, song_filepath:str):
        super().__init__()
        base_dir = Path(__file__).resolve().parent.parent
        self.path = (base_dir / song_filepath).resolve()
        self.audio = None
        self.length = None

        if not self.path.exists():
            raise FileNotFoundError(f"Song file not found: {self.path}")
    
        self.initialise_audio(self.path)

    def initialise_audio(self, path) -> Path:
        raise NotImplementedError

    def set(self, field: str, value:Any | None):
        raise NotImplementedError

    def path_as_url(self):
        return QUrl.fromLocalFile(self.path)

    def set_art(self,filepath: str):
        raise NotImplementedError

    def set_art_bytes(self, emit_update : bool, art_bytes: bytes | None):
        raise NotImplementedError
    
    def set_path(self):
        raise NotImplementedError

    def emit_update(self, emit_update : bool = True):
        if emit_update:
            self.changed.emit()
    
    def rename_file(self):
        path = self.set_path()
        self.initialise_audio(self.path)
        return path

    def update(self, **fields):
        for field, value in fields.items():
            self.set(field, value)
        self.audio.save()
        self.changed.emit()
    
    def silent_update(self, **fields):
        for field, value in fields.items():
            self.set(field, value)
        self.audio.save()

    
    def save(self) -> None:
        raise NotImplementedError

    def get_art(self) -> bytes | None:
        raise NotImplementedError

    def get_info(self, field):
        raise NotImplementedError
    
    def get_song_length(self) -> float:
        return float(self.length or 0.0)

