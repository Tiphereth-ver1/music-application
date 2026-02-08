from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from ...song import Song

class SongView(QWidget):
    def __init__(self, song: Song, parent=None):
        super().__init__(parent)
        self.song = song

        # --- Layout ---
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)

        # --- Song title label ---
        self.title_label = QLabel(song.get_info("title"))
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.addWidget(self.title_label)

        # --- time label (optional) ---
        self.time_label = QLabel(self._to_time(song.get_song_length()))
        self.time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.addWidget(self.time_label)

        # --- Optional: hover effect or styling ---
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
                border-radius: 5px;
            }
            QWidget:hover {
                background-color: #3e3e3e;
            }
        """)
    def _to_time(self, length) -> str:
        length = round(length)
        minutes = length // 60
        seconds = length % 60
        return f"{minutes}:{seconds:02d}"
