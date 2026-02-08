from PySide6.QtCore import Signal, QObject
from ...library_manager import LibraryService, AlbumMeta  # wherever AlbumMeta lives

class AlbumProvider(QObject):
    albums_changed = Signal(object)  # emit list[AlbumMeta]

    def __init__(self, library: LibraryService, parent=None):
        super().__init__(parent)
        self.lib = library
        self._albums: list[AlbumMeta] = []
        self.lib.library_changed.connect(self.refresh)
        self.refresh()

    def refresh(self) -> None:
        """Requery albums from DB and notify UI."""
        self._albums = self.lib.get_albums()
        self.albums_changed.emit(self._albums)

    def get_albums(self) -> list[AlbumMeta]:
        """Return cached album list (call refresh() at startup or after changes)."""
        return self._albums

    def get_album_song_ids(self, album_id: int) -> list[int]:
        return self.lib.get_album_song_ids(album_id)