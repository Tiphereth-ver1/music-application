from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)
import requests

from ...song import Song

class VideoPreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(300)
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.addStretch(1)

        # --- Cover label ---
        self.coverLabel = QLabel()
        self.coverLabel.setFixedSize(400, 225)
        self.coverLabel.setScaledContents(False)
        self.coverLabel.setAlignment(Qt.AlignCenter)
        self.internal_layout.addWidget(self.coverLabel, alignment=Qt.AlignCenter)

        # --- Song label ---
        self.song_label = QLabel()
        self.song_label.setAlignment(Qt.AlignCenter)
        self.internal_layout.addWidget(self.song_label)

    def update_preview(self, info: dict):
        title = info["Title"] or "Unknown Title"
        duration = info["Duration"] or "N/A"
        artist = info["Uploader"] or "Unknown Artist"
        thumbnail = info["Thumbnail"] or None

        self.song_label.setText(f"{title} ({duration}) \n{artist}")
        self.reload_image(thumbnail)

    # def _pixmap_from_url(self, url: str) -> QPixmap:
    #     r = requests.get(url, timeout=10)
    #     pix = QPixmap()
    #     pix.loadFromData(r.content)
    #     return pix


    def reload_image(self, image : bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        if pixmap:
            pixmap = pixmap.scaled(
                self.coverLabel.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            pixmap = QPixmap(250, 250)
            pixmap.fill(Qt.gray)

        self.coverLabel.setPixmap(pixmap)        