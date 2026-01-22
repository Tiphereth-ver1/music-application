from mutagen.flac import FLAC, Picture
from PySide6.QtCore import QUrl, Signal, QObject
from pathlib import Path
from typing import Any
import enum
from ..song import Song

TAG_MAP = {
    "title": "TITLE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "track": "TRACKNUMBER",
    "genre": "GENRE",
    "year": "DATE",
}

def _guess_mime(art_bytes: bytes) -> str:
    # JPEG magic: FF D8 FF
    if art_bytes.startswith(b"\xFF\xD8\xFF"):
        return "image/jpeg"
    # PNG magic: 89 50 4E 47 0D 0A 1A 0A
    if art_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    # Fallback (some players will still display it if mime is wrong, but try to be correct)
    return "application/octet-stream"


class FLACSong(Song):

    def __init__(self, song_filepath:str):
        super().__init__(song_filepath)

    def initialise_audio(self, path):
        self.audio = FLAC(path)
        if self.audio.tags is None:
            self.audio.add_tags() 
        self.length = float(self.audio.info.length)  # seconds

    def set(self, field: str, value: Any | None):
        try:
            key = TAG_MAP[field]
        except KeyError:
            raise ValueError(f"Unknown tag field: {field}")

        if value is None or value == "":
            # Clear the tag
            if key in self.audio:
                del self.audio[key]
            return
        
        self.audio[key] = [str(value)]

    def set_art(self, filepath: str):
        with open(filepath, "rb") as f:
            self.set_art_bytes(f.read())
    
    def set_art_bytes(self, emit_update : bool, art_bytes: bytes | None):
        self.audio.clear_pictures()

        if not art_bytes:
            self.save()
            self.changed.emit()
            return

        pic = Picture()
        pic.type = 3  # 3 = front cover
        pic.mime = _guess_mime(art_bytes)
        pic.desc = "Cover"
        pic.data = art_bytes

        self.audio.add_picture(pic)
        self.save()
        self.emit_update(emit_update)
    
    def get_info(self, field: str):
        try:
            key = TAG_MAP[field]
        except KeyError:
            raise ValueError(f"Unknown tag field: {field}")

        vals = self.audio.get(key)
        if not vals:
            return None

        # Mutagen returns list-like values for Vorbis comments
        return str(vals[0])
    
    def set_path(self) -> None:
        new_path = self.path.with_name(f'{self.get_info("title")}.flac')
        if self.path ==  new_path:
            print("Target name is already name of the file.")
            return
        if new_path.exists():
            raise FileExistsError(f"Target file already exists: {new_path}")

        self.path.rename(new_path)
        self.path = new_path


    def get_art(self) -> bytes | None:
        # Prefer front cover if present; else fallback to first picture.
        if not getattr(self.audio, "pictures", None):
            return None

        for pic in self.audio.pictures:
            if getattr(pic, "type", None) == 3:
                return pic.data

        return self.audio.pictures[0].data
    
    def save(self):
        self.audio.save()
