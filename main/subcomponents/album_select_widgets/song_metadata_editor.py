from PySide6.QtGui import (QPixmap, QIcon)
from PySide6.QtCore import (QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import ( QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QSizePolicy, QTextEdit, QLineEdit, 
    QVBoxLayout, QWidget, QPushButton, QFileDialog)

from ...song import Song
from pathlib import Path
import mimetypes
from enum import Enum

SINGLE_METADATA_FIELDS = [
    "title",
    "artist",
    "album",
    "album_artist",
    "track",
    "genre",
    "year",
]

ALBUM_METADATA_FIELDS = [
    "artist",
    "album",
    "album_artist",
    "genre",
    "year",
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


class SongMetadataEditor(QDialog):
    def __init__(self, mode, songs : list[Song], parent=None):
        super().__init__(parent)
        self.fields = {}
        self.songs = songs
        self.setWindowTitle("Edit Metadata")
        self.resize(400, 500)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setMinimumSize(QSize(400, 300))
        self.internal_layout = QVBoxLayout(self)
        self.art_bytes = songs[0].get_art()

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
        self._reload_preview(self.songs[0].get_art())
        self.internal_layout.addWidget(self.cover_button, alignment = Qt.AlignHCenter | Qt.AlignVCenter)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            parent=self
        )
        if mode == "single":
            fields = SINGLE_METADATA_FIELDS
        elif mode == "album":
            fields = ALBUM_METADATA_FIELDS

        for metadata in fields:
                field = MetadataField(metadata.lower(), self)
                self.internal_layout.addWidget(field)
                self.fields[metadata] = field
                field.set_value(self.songs[0].get_info(metadata))
            
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.internal_layout.addWidget(self.button_box)
        



    def _reload_preview(self, art_bytes):
        TARGET_SIZE = QSize(150, 150)
        if art_bytes:
            pixmap = QPixmap()
            pixmap.loadFromData(art_bytes)

            pixmap = pixmap.scaled(
                TARGET_SIZE,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            pixmap = QPixmap(150, 150)
            pixmap.fill(Qt.gray)

        self.cover_button.setIcon(QIcon(pixmap))
        self.cover_button.setIconSize(TARGET_SIZE)

    def get_metadata(self):
        return {
            key: field.value()
            for key, field in self.fields.items()
        }
    
    def select_new_art(self) -> bytes:
        ### QFileDialog opens up a file dialog selection screen
        filepath, _ = QFileDialog.getOpenFileName(
                self,
                "Select Album Art",
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
        if self.art_mime is None:
            self.art_mime = "image/jpeg"

        self._reload_preview(art_bytes)