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

from ...song import Song

class CoverSongLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QSize(500, 300))
        self.layout = QVBoxLayout(self)
        self.layout.setObjectName(u"layout")

        # --- Cover label ---
        self.coverLabel = QLabel()
        self.coverLabel.setFixedSize(250, 250)
        self.coverLabel.setScaledContents(False)
        self.coverLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.coverLabel, alignment=Qt.AlignCenter)

        # --- Song label ---
        self.song_label = QLabel()
        self.song_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.song_label)

    def update_now_playing(self,song: Song):
        if not song:
            self.song_label.setText("Nothing playing")
            return
        title = song.get_info("title") or "Unknown Title"
        artist = song.get_info("artist") or "Unknown Artist"
        self.song_label.setText(f"{title}\n{artist}")
        self.reload_image(song.get_art())


    def reload_image(self, art_bytes):
        if art_bytes:
            pixmap = QPixmap()
            pixmap.loadFromData(art_bytes)

            pixmap = pixmap.scaled(
                self.coverLabel.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            pixmap = QPixmap(250, 250)
            pixmap.fill(Qt.gray)

        self.coverLabel.setPixmap(pixmap)        

