from .song_search_components import SongItemDelegate, SongSerachListModel
from PySide6.QtWidgets import (QSizePolicy, QListView, QVBoxLayout, QWidget, QLineEdit)
from PySide6.QtCore import (Slot, Signal, QModelIndex)
from ..library_manager import LibraryService, PlaylistMeta


class SongSearchView(QWidget):
    returning_song = Signal(list, str)

    def __init__(self, library : LibraryService, parent = None):
        super().__init__(parent)
        self.playlist_id : int = None
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.internal_layout = QVBoxLayout(self)
        self.lib = library

        self.search_bar = QLineEdit(self)
        self.search_bar.textChanged.connect(self.refresh_songs)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.internal_layout.addWidget(self.search_bar)

        self.songs_list_view = QListView()
        self.songs_list_view.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.songs_list_model = SongSerachListModel(library)
        self.delegate = SongItemDelegate(self.songs_list_view)
        self.delegate.song_pressed.connect(self.return_song)
        self.songs_list_view.setItemDelegate(self.delegate)
        self.songs_list_view.setModel(self.songs_list_model)
        self.internal_layout.addWidget(self.songs_list_view, 3)
    
    def update_target_playlist(self, playlist : PlaylistMeta) -> None:
        self.playlist = playlist
    
    def refresh_songs(self):
        song_list = self.lib.get_matching_songs(self.search_bar.text())
        self.songs_list_model.update_song_ids(song_list)
        self.song_ids = self.songs_list_model._song_ids

    def return_song(self,idx, mode):
        song_id = self.song_ids[idx]
        self.returning_song.emit([song_id], mode)
        print(f"song return emitted on mode {mode}")



