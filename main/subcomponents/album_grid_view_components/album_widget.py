from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Signal, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar, QScrollArea,
    QVBoxLayout, QWidget)

from pathlib import Path
from ...library_manager import AlbumMeta

class AlbumWidget(QWidget):
    clicked = Signal()

    def __init__(self, album: AlbumMeta, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(250, 250)
        self.setAutoFillBackground(False)

        
        verticalLayout = QVBoxLayout(self)
        verticalLayout.setObjectName(u"verticalLayout")
        verticalLayout.setContentsMargins(-1, -1, 9, -1)

        self.CoverLabel = QLabel(self)
        self.CoverLabel.setObjectName(u"CoverLabel")
        self.CoverLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.CoverLabel.setFixedSize(QSize(150, 150))
        self.reload_preview(self.CoverLabel,album.cover_path)
        verticalLayout.addWidget(self.CoverLabel)

        self.title_label = QLabel(self)
        self.title_label.setText(album.title)
        verticalLayout.addWidget(self.title_label)
    
    def reload_preview(self, label: QLabel, art_source: bytes | Path | str | None):
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

    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


