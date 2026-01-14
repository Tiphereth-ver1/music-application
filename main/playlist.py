from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TYER, TDRC, TCON, COMM, APIC
from .song import Song
import logging

SORT_MODES = {
    "TITLE": lambda s: (s.get_info("title") or "").lower(),
    "ALBUM": lambda s: (s.get_info("album") or "").lower(),
    "ARTIST": lambda s: (s.get_info("artist") or "").lower(),
    
}

class Playlist:
    def __init__(self):
        self.songs : list[Song] = []
    
    def add_song(self, song: Song):
        self.songs.append(song)
    
    def remove_song(self, song):
        self.songs.remove(song)

    def show_list(self):
        for i, song in enumerate(self.songs, start=1):
            title = song.get_info("title") or "<untitled>"
            logging.info(f"{i}. {title}")
    
    def get_songs(self):
        return self.songs

    def sort_songs(self, mode="TITLE_ASC"):
        reverse = mode.endswith("DESC")
        key_func = SORT_MODES.get(mode, lambda s: "")
        self.songs.sort(key=key_func, reverse=reverse)
