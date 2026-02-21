from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy, QScrollArea,
    QSlider, QSpacerItem, QStackedWidget, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

from ...library_manager import LibraryService
from pathlib import Path

class CoverSongLabel(QWidget):
    def __init__(self, library : LibraryService, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QSize(500, 300))
        self.layout = QVBoxLayout(self)
        self.layout.setObjectName(u"layout")
        self.lib = library
        self.art_cache = library.art_cache

        # --- Cover label ---
        self.coverLabel = QLabel()
        self.coverLabel.setFixedSize(QSize(256,256))
        self.coverLabel.setScaledContents(False)
        self.coverLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.coverLabel, alignment=Qt.AlignCenter)

        # --- Song label ---
        self.song_label = QLabel()
        self.song_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.song_label)

    def update_now_playing(self, song_id: int):
        print(song_id)
        if not song_id:
            self.song_label.setText("Nothing playing")
            return
    
        meta = self.lib.get_song_meta(song_id)
        title = meta.title or "Unknown Title"
        artist = meta.artist or "Unknown Artist"
        self.song_label.setText(f"{title}\n{artist}")
        self.reload_preview(self.coverLabel, self.art_cache.get_image_cache(meta.art_hex,256))

    def reload_preview(self, label: QLabel, art_source: bytes | Path | str | None):
        pixmap = QPixmap()

        if isinstance(art_source, (Path, str)):
            # load from file path
            if pixmap.load(str(art_source)):
                pass
            else:
                pixmap = QPixmap(250, 250)
                pixmap.fill(Qt.gray)

        elif isinstance(art_source, (bytes, bytearray)) and art_source:
            # load from bytes
            pixmap.loadFromData(bytes(art_source))
            pass
        else:
            pixmap = QPixmap(250, 250)
            pixmap.fill(Qt.gray)

        label.setPixmap(pixmap)