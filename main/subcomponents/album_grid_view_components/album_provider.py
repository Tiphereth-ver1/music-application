from PySide6.QtCore import Signal, QObject
from ...library_manager import LibraryService, AlbumMeta, RETURN_VALUES  # wherever AlbumMeta lives
import time
class AlbumProvider(QObject):
    albums_changed = Signal(list)  # emit list[AlbumMeta]
    sorting_updated = Signal()

    def __init__(self, library: LibraryService, parent=None):
        super().__init__(parent)
        self.lib = library
        self._albums: list[AlbumMeta] = []
        self.lib.library_changed.connect(self.refresh)
        self.sorting_updated.connect(self.refresh)
        self.sort_mode : RETURN_VALUES = RETURN_VALUES.ID
        self.refresh()

    def update_sort_type(self, sort_mode : RETURN_VALUES):
        self.sort_mode = sort_mode
        self.sorting_updated.emit()

    def refresh(self) -> None:
        """Requery albums from DB and notify UI."""
        start = round(time.time()*1000)
        self._albums = self.lib.get_albums(self.sort_mode)
        end = round(time.time()*1000)
        print(f"recall time = {end-start}")
        self.albums_changed.emit(self._albums)

    def get_albums(self) -> list[AlbumMeta]:
        """Return cached album list (call refresh() at startup or after changes)."""
        return self._albums

    def get_album_song_ids(self, album_id: int) -> list[int]:
        return self.lib.get_album_song_ids(album_id)