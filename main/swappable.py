from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal

from .subcomponents import AlbumGridView, PlayerView, AlbumSelect, DownloaderView

class Swappable(QWidget):
    returning_song = Signal(object, str)
    updating_view = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.album_view = AlbumGridView(self.stack)
        self.player_view = PlayerView(self.stack)
        self.downloader_view = DownloaderView(self.stack)
        self.album_select = None

        # self.album_view.setStyleSheet("background-color: lightblue;")
        # self.player_view.setStyleSheet("background-color: lightgreen;")

        self.album_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.downloader_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        self.stack.addWidget(self.album_view)
        self.stack.addWidget(self.player_view)
        self.stack.addWidget(self.downloader_view)

        # default visible page
        self.stack.setCurrentWidget(self.album_view)
        self.album_view.album_clicked.connect(self.show_album_select)
        self.downloader_view.updating_view.connect(self.update_view)


    
    def show_album_select(self, album):
        if self.album_select is not None:
            self.stack.removeWidget(self.album_select)
            self.album_select.deleteLater()
        
        self.album_select = AlbumSelect(album, self.stack)
        self.album_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.addWidget(self.album_select)
        self.stack.setCurrentWidget(self.album_select)
        self.album_select.back_button.clicked.connect(self.back_to_album_grid)
        self.album_select.returning_song.connect(self.return_song)


    def back_to_album_grid(self):
        self.stack.setCurrentWidget(self.album_view)
        if self.album_select:
            self.stack.removeWidget(self.album_select)
            self.album_select.deleteLater()
            self.album_select = None
    
    def return_song(self, song, mode):
        self.returning_song.emit(song, mode)
    
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
