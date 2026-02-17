from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal

from .subcomponents import AlbumGridView, SongSearchView, PlayerView, PlaylistGridView, AlbumSelect, DownloaderView, PlaylistSelect
from .subcomponents.playlist_grid_view_components import PlaylistProvider
from .library_manager import LibraryService

class Swappable(QWidget):
    perform_action = Signal(str)
    returning_song = Signal(object, str)
    updating_view = Signal()
    def __init__(self, library : LibraryService, parent=None):
        super().__init__(parent)
        self.lib = library
        self.playlist_provider = PlaylistProvider(library)

        # layout for this widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setMinimumSize(700, 0)


        # container for stacked UI pages
        self.stack = QStackedWidget(self)
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.stack)
        

        # your pages
        self.album_view = AlbumGridView(library, self.stack)
        self.playlist_view = PlaylistGridView(library, self.playlist_provider, self.stack)
        self.player_view = PlayerView(self.lib, self.stack)
        self.downloader_view = DownloaderView(self.lib, self.stack)
        self.song_search_view = SongSearchView(self.lib, self.stack)
        self.album_select = None
        self.playlist_select = None

        # self.album_view.setStyleSheet("background-color: lightblue;")
        # self.player_view.setStyleSheet("background-color: lightgreen;")

        self.album_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.downloader_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.playlist_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.song_search_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.stack.addWidget(self.player_view)
        self.stack.addWidget(self.song_search_view)
        self.stack.addWidget(self.playlist_view)
        self.stack.addWidget(self.album_view)
        self.stack.addWidget(self.downloader_view)

        # default visible page
        self.stack.setCurrentWidget(self.album_view)
        self.album_view.album_clicked.connect(self.show_album_select)
        self.playlist_view.playlist_clicked.connect(self.show_playlist_select)
        self.downloader_view.updating_view.connect(self.update_view)
        self.song_search_view.returning_song.connect(self.return_songs)
        self.player_view.perform_action.connect(self.send_action)

    def show_album_select(self, album):
        if self.album_select is not None:
            self.stack.removeWidget(self.album_select)
            self.album_select.deleteLater()
        
        self.album_select = AlbumSelect(self.lib, album, self.stack)
        self.album_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.addWidget(self.album_select)
        self.stack.setCurrentWidget(self.album_select)
        self.album_select.back_button.clicked.connect(self.back_to_album_grid)
        self.album_select.returning_song.connect(self.return_songs)
        self.album_select.returning_album.connect(self.return_songs)

    def send_action(self, action : str):
        self.perform_action.emit(action)

    def back_to_album_grid(self):
        self.stack.setCurrentWidget(self.album_view)
        if self.album_select:
            self.stack.removeWidget(self.album_select)
            self.album_select.deleteLater()
            self.album_select = None
    
    def show_playlist_select(self, playlist):
        if self.playlist_select is not None:
            self.stack.removeWidget(self.playlist_select)
            self.playlist_select.deleteLater()
        
        self.playlist_select = PlaylistSelect(self.lib, self.playlist_provider, playlist, self.stack)
        self.playlist_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.addWidget(self.playlist_select)
        self.stack.setCurrentWidget(self.playlist_select)
        self.playlist_select.back_button.clicked.connect(self.back_to_playlist_grid)
        self.playlist_select.returning_song.connect(self.return_songs)
        self.playlist_select.returning_playlist.connect(self.return_songs)
        self.playlist_select.toggle_add_mode.connect(self.song_search_view.update_target_playlist)

    def back_to_playlist_grid(self):
        self.stack.setCurrentWidget(self.playlist_view)
        if self.playlist_select:
            self.stack.removeWidget(self.playlist_select)
            self.playlist_select.deleteLater()
            self.playlist_select = None

    def return_songs(self, songs, mode):
        self.returning_song.emit(songs, mode)
    
    def update_view(self):
        self.updating_view.emit()

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Swappable Test")
    window.resize(900, 600)

    swappable = Swappable()
    window.setCentralWidget(swappable)

    window.show()

    sys.exit(app.exec())
