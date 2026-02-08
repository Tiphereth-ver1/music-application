from mutagen.mp4 import MP4, MP4Cover
from enum import Enum
from ..song import Song, sanitize_filename
from typing import Any



class Tags(Enum):
    TITLE = "©nam"
    ARTIST =  "©ART"
    ALBUM = "©alb"
    ALBUM_ARTIST = "aART"
    TRACK = "trkn"
    GENRE = "©gen"
    YEAR = "©day"


TAG_MAP = {
    "title": Tags.TITLE,
    "artist": Tags.ARTIST,
    "album": Tags.ALBUM,
    "album_artist": Tags.ALBUM_ARTIST,
    "track": Tags.TRACK,
    "genre": Tags.GENRE,
    "year": Tags.YEAR,
}

def _guess_cover_format(art_bytes: bytes) -> str:
    # JPEG magic: FF D8 FF
    if art_bytes.startswith(b"\xFF\xD8\xFF"):
        return MP4Cover.FORMAT_JPEG
    # PNG magic: 89 50 4E 47 0D 0A 1A 0A
    if art_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return MP4Cover.FORMAT_PNG
    raise ValueError("Unknown image format (not PNG or JPEG)")


def _coerce_int(x: Any) -> int:
    # Accept "07", 7, 7.0, etc. Reject nonsense early.
    if x is None or x == "":
        raise ValueError("Empty value")
    return int(x)


class M4ASong(Song):

    def __init__(self, song_filepath:str):
        super().__init__(song_filepath)

    def initialise_audio(self, path):
        pass
        self.audio = MP4(path)
        if self.audio.tags is None:
            self.audio.add_tags() 
        self.length = self.audio.info.length
    
    def _get_trkn(self) -> tuple[int, int]:
        """Return (track, total) from current tags, defaulting to (0, 0)."""
        raw = self.audio.tags.get("trkn")
        if not raw:
            return (0, 0)
        t, tot = raw[0]
        return (int(t or 0), int(tot or 0))


    def set(self, field: str, value: Any | None):
        try:
            tag : Tags = TAG_MAP[field]
        except KeyError:
            raise ValueError(f"Unknown tag field: {field}")
        
        key = tag.value
        if value is None or value == "":
            if tag.value in self.audio:
                del self.audio[tag.value]
            return
        
        if field == "track":
            track, total = self._get_trkn()
            track = _coerce_int(value)
            self.audio.tags["trkn"] = [(track, total)]
            return

        if field == "track_total":
            track, total = self._get_trkn()
            total = _coerce_int(value)
            self.audio.tags["trkn"] = [(track, total)]
            return
        
        self.audio.tags[key] = [str(value)]

    def get_info(self, field: str):
        try:
            tag = TAG_MAP[field]
        except KeyError:
            raise ValueError(f"Unknown tag field: {field}")

        if field == "track":
            track, _ = self._get_trkn()
            return track if track != 0 else None

        if field == "track_total":
            _, total = self._get_trkn()
            return total if total != 0 else None

        key = tag.value
        vals = self.audio.tags.get(key)
        if not vals:
            return None
        return vals[0] 


    def set_art(self,filepath: str):
        with open(filepath, "rb") as albumart:
            img_bytes = albumart.read()
            # Pick the right MP4Cover "imageformat"
            if filepath.lower().endswith((".jpg", ".jpeg")):
                fmt = MP4Cover.FORMAT_JPEG
            elif filepath.lower().endswith(".png"):
                fmt = MP4Cover.FORMAT_PNG
            else:
                raise ValueError("Cover image must be .jpg/.jpeg or .png for MP4 tags")

            self.audio["covr"] = [MP4Cover(img_bytes, imageformat=fmt)]
            self.audio.save()
            self.changed.emit()
    
    def set_art_bytes(self, emit_update, art_bytes: bytes):
        format = _guess_cover_format(art_bytes)
        self.audio["covr"] = [MP4Cover(art_bytes, imageformat=format)]
        self.audio.save()
        self.emit_update(emit_update)

    def set_path(self) -> None:
        new_path = self.path.with_name(sanitize_filename(f'{self.get_info("title")}.m4a'))
        if self.path ==  new_path:
            print("Target name is already name of the file.")
            return
        if new_path.exists():
            raise FileExistsError(f"Target file already exists: {new_path}")

        self.path.rename(new_path)
        self.path = new_path
        return self.path
            
    def get_art(self) -> bytes | None:
        """Return the raw album art bytes, if any."""
        covers = self.audio.tags.get("covr")
        if not covers:
            return None

        cover: MP4Cover = covers[0]
        image_bytes = bytes(cover)
        if image_bytes:
            return image_bytes
        return None
    
    def save(self) -> None:
        self.audio.save()