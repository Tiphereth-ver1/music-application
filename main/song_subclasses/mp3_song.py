from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TYER, TDRC, TCON, COMM, APIC
from PySide6.QtCore import QUrl, Signal, QObject
from pathlib import Path
import enum
from ..song import Song

TAG_MAP = {
    "title": TIT2,
    "artist": TPE1,
    "album": TALB,
    "track": TRCK,
    "genre": TCON,
    "year": TDRC,
}

class MP3Song(Song, QObject):

    def __init__(self, song_filepath:str):
        super().__init__(song_filepath)

    def initialise_audio(self, path):
        pass
        self.audio = MP3(path, ID3 = ID3)
        if self.audio.tags is None:
            self.audio.add_tags() 
        self.length = self.audio.info.length

    def set(self, field: str, value:str | None):
        try:
            frame_cls = TAG_MAP[field]
        except KeyError:
            raise ValueError(f"Unknown tag field: {field}")
        
        frame_id = frame_cls.__name__
        
        if value is None:
            self.audio.pop(frame_id, None)
            return

        self.audio[frame_cls.__name__] = frame_cls(
            encoding=3,
            text=value
        )

    def set_art(self,filepath: str):
        self.audio.tags.delall('APIC')
        with open(filepath, "rb") as albumart:
            self.audio['APIC'] = APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=albumart.read()
        )
        self.audio.save(v2_version=3)
        self.changed.emit()
    
    def set_art_bytes(self,emit_update : bool, art_bytes: bytes):
        self.audio.tags.delall('APIC')
        self.audio['APIC'] = APIC(
        encoding=3,
        mime='image/jpeg',
        type=3,
        desc='Cover',
        data=art_bytes)
        self.audio.save(v2_version=3)
        self.emit_update(emit_update)
    
    def set_path(self) -> None:
        new_path = self.path.with_name(f'{self.get_info("title")}.mp3')
        if self.path ==  new_path:
            print("Target name is already name of the file.")
            return
        if new_path.exists():
            raise FileExistsError(f"Target file already exists: {new_path}")

        self.path.rename(new_path)
        self.path = new_path

    def update(self, **fields):
        for field, value in fields.items():
            self.set(field, value)
        self.changed.emit()
        self.audio.save(v2_version=3)
        
    def get_art(self) -> bytes | None:
        """Return the raw album art bytes, if any."""
        apic_frames = self.audio.tags.getall("APIC")
        if apic_frames:
            return apic_frames[0].data
        return None
    
    def get_info(self, field):
        try:
            frame_cls = TAG_MAP[field]
        except KeyError:
            raise ValueError(f"Unknown tag field: {field}")

        frame = self.audio.get(frame_cls.__name__)
        if not frame:
            return None

        return frame.text[0]
    
    def get_song_length(self) -> float:
        return self.length


    def get_all_info(self):
        print("Song Information \n________________________")
        for name, tag in TAG_MAP.items():
            frame = self.audio.get(tag.__name__)
            if frame:
                print(f"{name}: {frame}")
            else:
                print(f"{name}: <not set>")
        print("________________________")

    def save(self):
        self.audio.save(v2_version=3)