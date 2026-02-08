from PySide6.QtGui import (QPixmap, QIcon)
from PySide6.QtCore import (QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import ( QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QSizePolicy, QTextEdit, QLineEdit, 
    QVBoxLayout, QWidget, QPushButton, QFileDialog)

from ...song import Song
from pathlib import Path
import mimetypes
from enum import Enum

FIELDS = [
    "name",
]



class MetadataField(QWidget):
    def __init__(self, label: str, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setMinimumHeight(30)
        self.setMaximumHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label)
        self.label.setMinimumWidth(80)  # optional alignment
        self.label.setText(label)
        layout.addWidget(self.label)

        self.editor = QLineEdit()
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.editor.setMinimumHeight(30)
        layout.addWidget(self.editor)

    def value(self) -> str:
        return self.editor.text()

    def set_value(self, value):
        if value is None:
            self.editor.clear()
        else:
            self.editor.setText(str(value))

    ### For you tmrw to go through:
    # fixing the the metadata editor
    # modify_song notation
    # some stuff in album_song_list and how the listview is generated

from ...library_manager import PlaylistMeta, LibraryService
class PlaylistEditor(QDialog):
    def __init__(self, library, LibraryService, playlist_meta : PlaylistMeta, parent=None):
        super().__init__(parent)
        self.fields = {}
        self.lib = library
        self.playlist_meta = playlist_meta
        self.setWindowTitle("Edit Metadata")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.internal_layout = QVBoxLayout(self)
        self.cover_path = self.playlist_meta.cover_path

        self.cover_button = QPushButton(self)

        self.cover_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent; /* Makes background match parent widget */
                text-align: center;
                padding: 0; /* Remove default padding */
            }
            QPushButton:hover {
                background-color: transparent; /* No background change on hover */
            }
            QPushButton:pressed {
                background-color: transparent; /* No background change when pressed */
            }
        """)


        self.cover_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.cover_button.setMinimumSize(QSize(150, 150))
        self.cover_button.clicked.connect(self.select_new_art)
        self.reload_preview(self.cover_button, self.cover_path)
        self.internal_layout.addWidget(self.cover_button, alignment = Qt.AlignHCenter | Qt.AlignVCenter)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            parent=self
        )

        for metadata in FIELDS:
                field = MetadataField(metadata.lower(), self)
                self.internal_layout.addWidget(field)
                self.fields[metadata] = field
                self.fields[metadata].set_value(self.playlist_meta.name)
            
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.internal_layout.addWidget(self.button_box)

    def reload_preview(self, label: QLabel, art_source: bytes | Path | str | None):
        TARGET_SIZE = QSize(150, 150)
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

        self.cover_button.setIcon(QIcon(pixmap))
        self.cover_button.setIconSize(TARGET_SIZE)


    def get_info(self):
        print(self.fields["name"].value(),str(self.cover_path))
        return self.fields["name"].value(),str(self.cover_path)

    
    def select_new_art(self) -> bytes:
        ### QFileDialog opens up a file dialog selection screen
        filepath, _ = QFileDialog.getOpenFileName(
                self,
                "Select Playlist Art",
                "",
                "Images (*.png *.jpg *.jpeg *.webp)"
            )

        if not filepath:
                return

        path = Path(filepath)

        try:
            art_bytes = path.read_bytes()
        except OSError:
            return

        self.art_bytes = art_bytes
        self.art_mime, _ = mimetypes.guess_type(filepath)
        self.cover_path = path
        if self.art_mime is None:
            self.art_mime = "image/jpeg"

        self.reload_preview(self.cover_button, art_bytes)
