from .album import Album
from typing import List, Optional
from ...song import Song
from pathlib import Path
from PySide6.QtCore import Signal, QObject


class AlbumIndexer(QObject):
    album_changed = Signal(object)
    # This is an example of a class that uses cacheing in order to improve its performance. So what does cacheing do?
    # - Cacheing allows the storing of certain parameters that have no need to be constantly recalculated.
    # - Cacheing is best used when you have a single source of truth which other elements are derived from.
    # - In this particular case, the song list is the truth, and the other factors (albums) are derived from this.
    # - The only time the album view needs to be recompiled is when there is a change to this source of truth, which is the purpose of the dirty marker.
    # - Notice how it is only located on set_songs() and add_songs() here
    # - There are also different types of cacheing that update at different times.
    #     * Eager cacheing will always immediately replace the album data when there is a change (not here).
    #     * Lazy cacheing (the one used in this case) only replaces the album data when it is strictly needed (notice _check_albums() attached to certain functions)
    # - There are other types of cacheing as well but I'm a little dumb so I'm not going to cover them here
    
    # Long Pham

    def __init__(self, parent = None):
        super().__init__()
        self.songs : list[Song] = []
        self._albums: dict[tuple[str,str], Album] = {}
        self._dirty = False
    
    def set_songs(self, songs: list[Song]):
        self.songs.clear()
        self.songs.extend(songs)
        self._dirty = True
        for song in songs:
            song.changed.connect(self._on_song_changed)
    
    def add_songs(self, songs: list[Song]):
        self.songs.extend(songs)
        self._dirty = True
        for song in songs:
            song.changed.connect(self._on_song_changed)

    
    def remove_songs(self, songs: list[Song]):
        for song in songs:
            if song in self.songs:
                self.songs.remove(song)
            

    def _build_albums(self, songs: List[Song]):
        for song in songs:
            key = (song.get_info("album"), song.get_info("artist"))
            if key in self._albums:
                self._albums[key].add_song(song)
            else:
                new_album = Album(*key)
                new_album.add_song(song)
                self._albums[key] = new_album
        self._dirty = False
        self.album_changed.emit(self._albums.values())

    def _on_song_changed(self):
        self._dirty = True
        self._check_albums()


    def _check_albums(self):
        if self._dirty:
            self.clear_albums()
            self._build_albums(self.songs)

    def clear_albums(self):
        self._albums.clear()
        
    def get_albums(self) -> list[Album]:
        self._check_albums()
        return list(self._albums.values())

    def print_albums(self):
        self._check_albums()
        for album in self._albums.values():
            info = album.info_check()
            print(f"{info[0]}: {info[1]}")
    
    def filepath_to_songs(self):
        base_dir = Path(__file__).resolve().parent.parent
        music_folder = base_dir / "music"
        songs = []
        for file_path in music_folder.rglob("*.mp3"):
            rel_path = file_path.relative_to(base_dir)
            songs.append(Song(rel_path))
        return songs