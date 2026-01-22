from PySide6.QtCore import (QSize, Qt, Signal)
from PySide6.QtGui import (QPixmap, QFont)

from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget, QPushButton, QListView, QDialog)

from .album_grid_view_components import Album
from .album_select_widgets import AlbumSongListModel, SongItemDelegate, SongMetadataEditor, ButtonBox
from ..song import Song

class AlbumSelect(QWidget):
    returning_song = Signal(list, str)
    returning_album = Signal(list, str)

    def __init__(self, album : Album, parent = None):
        super().__init__(parent)
        self.internal_layout = QVBoxLayout(self)
        self.album = album

        self.cover_title_box = QWidget(self)
        self.cover_title_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.cover_title_box.setMinimumSize(QSize(600, 250))
        self.cover_title_box_layout = QHBoxLayout(self.cover_title_box)
        self.cover_Label = QLabel(self.cover_title_box)
        self.cover_Label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.cover_Label.setMinimumSize(QSize(200, 200))
        
        self.text_font = QFont()
        self.title_button_box = QWidget(self.cover_title_box)
        self.title_button_box_layout = QVBoxLayout(self.title_button_box)
        self.title_button_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.text_font.setPointSize(16)
        self.title_Label = QLabel(self.title_button_box)
        self.title_Label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.title_Label.setFont(self.text_font)

        self.cover_title_box_layout.addWidget(self.cover_Label)
        self.title_button_box_layout.addWidget(self.title_Label,alignment= Qt.AlignLeft | Qt.AlignBottom)

        self.buttons = ButtonBox(self)
        self.buttons.add_queue_album.connect(self.return_album)
        self.buttons.edit_album.connect(self.modify_songs)
        self.title_button_box_layout.addWidget(self.buttons)
        self.cover_title_box_layout.addWidget(self.title_button_box)

        self.internal_layout.addWidget(self.cover_title_box)


        self.song_view = QListView()
        self.album_model = AlbumSongListModel(album)
        self.delegate = SongItemDelegate(self.song_view)
        self.song_view.setItemDelegate(self.delegate)
        self.delegate.song_pressed.connect(self.return_song)
        self.delegate.to_modify_song.connect(self.modify_songs)

        self.song_view.setModel(self.album_model)
        self.song_view.setIconSize(QSize(40,40))  # must set icon size

        self.internal_layout.addWidget(self.song_view)
        self.update_ui()

        # --- Back button ---
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedHeight(40)
        self.internal_layout.addWidget(self.back_button)

    def _reload_preview(self, art_bytes):
        if art_bytes:
            pixmap = QPixmap()
            pixmap.loadFromData(art_bytes)

            pixmap = pixmap.scaled(
                self.cover_Label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            pixmap = QPixmap(200, 200)
            pixmap.fill(Qt.gray)

        self.cover_Label.setPixmap(pixmap)
        
    def update_ui(self):
        songs = self.album.get_songs()
        info = self.album.info_check()
        self.title_Label.setText(f"{info[0]} \n{info[1]}")
        length = len(songs)
        self._reload_preview(self.album.get_cover())

    def return_song(self,idx, mode):
        song = self.album.get_song(idx)
        self.returning_song.emit([song], mode)
        print(f"song return emitted on mode {mode}")
    
    def return_album(self, mode):
        self.returning_album.emit(self.album.songs, mode)
    
    def modify_songs(self, mode, idx = None):
        if mode == "album":
            songs = self.album.get_songs()
            dialog = SongMetadataEditor("album", songs, self)
            if dialog.exec() == QDialog.Accepted:
                try:
                    for song in songs:
                        song.silent_update(**dialog.get_metadata())
                        if dialog.art_bytes:
                            song.set_art_bytes(False, dialog.art_bytes)
                finally:
                    songs[0].emit_update(True)
    
        elif mode == "single":
            song = self.album.get_song(idx)
            dialog = SongMetadataEditor("single", [song], self)
            if dialog.exec() == QDialog.Accepted:
                song.update(**dialog.get_metadata())
                if dialog.art_bytes:
                    song.set_art_bytes(dialog.art_bytes)