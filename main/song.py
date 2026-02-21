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
    """
    Replace illegal characters in Windows filenames and reserved device names.

    :param name: The string to sanitize.
    :type name: str
    :param replacement: String to replace illegal characters with.
    :type replacement: str
    :param max_length: Maximum allowed length of the output string.
    :type max_length: int
    :return: The sanitized filename.
    :rtype: str
    """
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
    """
    Abstract base class representing a standardized interface for audio files.

    This class defines the common behaviour required for working with different
    audio metadata/format backends. Subclasses are responsible for loading
    audio data, providing metadata access, and managing album art and file paths.

    Each subclass must implement the following methods:

    - initialise_audio(path): Load the audio file located at ``path`` and assign
      an appropriate backend object to ``self.audio``. This method should also
      populate ``self.length`` if available.
    - set(field, value): Update a metadata field (e.g. title, artist, album).
      Implementations may raise ValueError for unsupported fields.
    - set_art(filepath): Set the embedded artwork using an image file.
    - set_art_bytes(emit_update, art_bytes): Set the embedded artwork from raw
      bytes and optionally emit an update signal.
    - set_path(): Compute and apply a new filesystem path for the song based on
      subclass rules. Must return the new path.
    - save(): Persist metadata and artwork changes to disk.
    - get_art(): Return embedded artwork as bytes or ``None``.
    - get_info(field): Return the requested metadata value.

    Attributes:
        path (Path): Absolute path to the audio file.
        audio: Backend-specific audio object that provides loading and saving.
        length (float | None): Duration of the song in seconds, set by the
            subclass during audio initialisation.

    Notes:
        - ``update()`` applies field updates and emits ``changed``.
        - ``silent_update()`` applies field updates without emitting ``changed``.
        - ``path_as_url()`` provides a ``QUrl`` suitable for Qt file-handling.
        - ``rename_file()`` delegates filename generation to ``set_path()`` and
          reloads audio metadata.

    Example:
        class MP3Song(Song):
            def initialise_audio(self, path):
                self.audio = MutagenMP3(path)
                self.length = self.audio.info.length
                return path

            def set(self, field, value):
                self.audio.tags[field] = value
    """
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

