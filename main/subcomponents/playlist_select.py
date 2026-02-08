from PySide6.QtCore import (QSize, Qt, Signal)
from PySide6.QtGui import (QPixmap, QFont)

from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget, QPushButton, QListView, QDialog)

from ..library_manager import PlaylistMeta, LibraryService
from .playlist_select_widgets import PlaylistSongListModel, SongItemDelegate, PlaylistEditor, ButtonBox
from ..song import Song
from pathlib import Path

class PlaylistSelect(QWidget):
    returning_song = Signal(list, str)
    returning_playlist = Signal(list, str)

    def __init__(self, library: LibraryService, playlist_meta: PlaylistMeta, parent=None):
        super().__init__(parent)
        self.internal_layout = QVBoxLayout(self)
        self.lib = library
        self.playlist_meta = playlist_meta
        self.song_ids = self.lib.get_songs_from_playlist(self.playlist_meta.id)

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
        self.buttons.add_queue_playlist.connect(self.return_playlist)
        self.buttons.edit_playlist.connect(self.modify_playlist)
        self.title_button_box_layout.addWidget(self.buttons)
        self.cover_title_box_layout.addWidget(self.title_button_box)

        self.internal_layout.addWidget(self.cover_title_box)


        self.song_view = QListView()
        self.playlist_model = PlaylistSongListModel(self.lib, playlist_meta)
        self.delegate = SongItemDelegate(self.song_view)
        self.song_view.setItemDelegate(self.delegate)
        self.delegate.song_pressed.connect(self.return_song)

        self.song_view.setModel(self.playlist_model)
        self.song_view.setIconSize(QSize(40,40))  # must set icon size

        self.internal_layout.addWidget(self.song_view)
        self.update_ui()

        # --- Back button ---
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedHeight(40)
        self.internal_layout.addWidget(self.back_button)

    def _reload_preview(self, label: QLabel, art_source: bytes | Path | str | None):
        pixmap = QPixmap()

        if isinstance(art_source, (Path, str)):
            # load from file path
            if pixmap.load(str(art_source)):
                pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                pixmap = QPixmap(150, 150)
                pixmap.fill(Qt.gray)

        elif isinstance(art_source, (bytes, bytearray)) and art_source:
            # load from bytes
            pixmap.loadFromData(bytes(art_source))
            pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        else:
            pixmap = QPixmap(150, 150)
            pixmap.fill(Qt.gray)

        label.setPixmap(pixmap)

        
    def update_ui(self):
        song_ids = self.lib.get_songs_from_playlist(self.playlist_meta.id)
        name = self.playlist_meta.name
        self.title_Label.setText(f"{name}")
        length = len(song_ids)
        self._reload_preview(self.cover_Label, self.playlist_meta.cover_path)

    def return_song(self,idx, mode):
        song_id = self.song_ids[idx]
        self.returning_song.emit([song_id], mode)
        print(f"song return emitted on mode {mode}")
    
    def return_playlist(self, mode):
        self.returning_playlist.emit(list(self.song_ids), mode)
    
    def modify_playlist(self):
        print("dialog opened")
        dialog = PlaylistEditor(self, self.lib, self.playlist_meta)
        if dialog.exec() == QDialog.Accepted:
            try:
                name, cover_path = dialog.get_info()
                print(self.playlist_meta.id)
                self.lib.modify_playlist(self.playlist_meta.id, name, cover_path)
            finally:
                pass
        self.lib.post_playlist_edit_check()