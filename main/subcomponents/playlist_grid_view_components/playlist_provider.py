from PySide6.QtCore import Signal, QObject
from ...library_manager import LibraryService, PlaylistMeta
import logging 

class PlaylistProvider(QObject):
    playlists_changed = Signal(object) 

    def __init__(self, library: LibraryService, parent=None):
        super().__init__(parent)
        self.lib = library
        self._playlists: list[PlaylistMeta] = []
        self.lib.playlists_changed.connect(self.refresh)
        self.refresh()

    def refresh(self) -> None:
        """Requery playlist from DB and notify UI."""
        logging.debug("refresh triggered")
        self._playlists = self.lib.get_playlists()
        self.playlists_changed.emit(self._playlists)

    def get_playlists(self) -> list[PlaylistMeta]:
        """Return cached playlist list (call refresh() at startup or after changes)."""
        return self._playlists

    def get_playlist_song_ids(self, playlist_id: int) -> list[int]:
        return self.lib.get_playlist_song_ids(playlist)