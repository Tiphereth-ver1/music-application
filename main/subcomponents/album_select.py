from PySide6.QtCore import (QSize, Qt, Signal)
from PySide6.QtGui import (QPixmap, QFont)

from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget, QPushButton, QListView, QDialog)

from ..library_manager import AlbumMeta, LibraryService
from .album_select_widgets import AlbumSongListModel, SongItemDelegate, SongMetadataEditor, ButtonBox
from ..song import Song
from pathlib import Path

class AlbumSelect(QWidget):
    returning_song = Signal(list, str)
    returning_album = Signal(list, str)

    def __init__(self, library: LibraryService, album_meta: AlbumMeta, parent=None):
        super().__init__(parent)
        self.internal_layout = QVBoxLayout(self)
        self.lib = library
        self.album_meta = album_meta
        self.song_ids = self.lib.get_album_song_ids(self.album_meta.id)

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
        self.album_model = AlbumSongListModel(self.lib, album_meta)
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
        song_ids = self.lib.get_album_song_ids(self.album_meta.id)
        title, artist = self.album_meta.title, self.album_meta.album_artist
        self.title_Label.setText(f"{title} \n{artist}")
        length = len(song_ids)
        self._reload_preview(self.cover_Label, self.album_meta.cover_path)

    def return_song(self,idx, mode):
        song_id = self.song_ids[idx]
        self.returning_song.emit([song_id], mode)
        print(f"song return emitted on mode {mode}")
    
    def return_album(self, mode):
        self.returning_album.emit(list(self.song_ids), mode)
    
    def modify_songs(self, mode, idx = None):
        if mode == "album":
            songs = self.lib.songs_from_ids(self.song_ids)
            dialog = SongMetadataEditor("album", songs, self)
            if dialog.exec() == QDialog.Accepted:
                try:
                    for song in songs:
                        song.silent_update(**dialog.get_metadata())
                        if dialog.art_bytes:
                            song.set_art_bytes(False, dialog.art_bytes)
                    for song_id in self.song_ids:
                        self.lib.invalidate_song(song_id)
                        abs_path = self.lib.abs_song_path(song_id)
                        self.lib.upsert_song_from_path(abs_path)
                finally:
                    songs[0].emit_update(True)
    
        elif mode == "single":
            song_id = self.song_ids[idx]
            abs_path = self.lib.abs_song_path(song_id)
            song = self.lib.SongFactory(song_id)
            dialog = SongMetadataEditor("single", [song], self)
            if dialog.exec() == QDialog.Accepted:
                song.update(**dialog.get_metadata())
                self.lib.invalidate_song(song_id)
                self.lib.upsert_song_from_path(abs_path)
                if dialog.art_bytes:
                    song.set_art_bytes(True, dialog.art_bytes)
        self.lib.invalidate_album_cache(self.album_meta.id)
        self.lib.post_album_edit_check()