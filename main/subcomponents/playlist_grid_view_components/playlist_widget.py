from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Signal, Qt, QTimer)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar, QScrollArea,
    QVBoxLayout, QWidget)

from pathlib import Path
from ...library_manager import PlaylistMeta
from ...art_cache import ArtCache

class PlaylistWidget(QWidget):
    clicked = Signal()

    def __init__(self, playlist: PlaylistMeta, art_cache: ArtCache, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(250, 250)
        self.setAutoFillBackground(False)
        self.art_cache = art_cache
        self.playlist = playlist

        verticalLayout = QVBoxLayout(self)
        verticalLayout.setObjectName(u"verticalLayout")
        verticalLayout.setContentsMargins(-1, -1, 9, -1)

        _PLACEHOLDER = QPixmap(128, 128)
        _PLACEHOLDER.fill(Qt.gray)


        print(playlist.art_hex)
        self.cover_label = QLabel(self)
        self.cover_label.setObjectName(u"cover_label")
        self.cover_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cover_label.setFixedSize(QSize(128, 128))
        self.cover_label.setPixmap(_PLACEHOLDER)
        verticalLayout.addWidget(self.cover_label)

        self.title_label = QLabel(self)
        self.title_label.setText(playlist.title)
        verticalLayout.addWidget(self.title_label)
        QTimer.singleShot(50, self.refresh_cover)
    
    def reload_preview(self, label: QLabel, art_source: bytes | Path | str | None):
        pixmap = QPixmap()

        if isinstance(art_source, (Path, str)):
            # load from file path
            if pixmap.load(str(art_source)):
                pass
            else:
                pixmap = QPixmap(128, 128)
                pixmap.fill(Qt.gray)

        elif isinstance(art_source, (bytes, bytearray)) and art_source:
            # load from bytes
            pixmap.loadFromData(bytes(art_source))
            pass

        else:
            pixmap = QPixmap(128, 128)
            pixmap.fill(Qt.gray)

        label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def refresh_cover(self):
        if not self.playlist.art_hex:
            return
        path = self.art_cache.get_image_cache(self.playlist.art_hex, 128)
        self.reload_preview(self.cover_label, path)
    
    def set_playlist(self, playlist : PlaylistMeta):
        self.title_label.setText(playlist.title)
        path = self.art_cache.get_image_cache(playlist.art_hex, 128)
        self.reload_preview(self.cover_label, path)
