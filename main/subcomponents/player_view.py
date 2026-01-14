from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QSizePolicy,QVBoxLayout, QWidget)
from .player_view_widgets import CoverSongLabel, ShuffleLoop, SongTime, Volume, PreviousPauseNext

class PlayerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(QSize(520, 640))
        self.layout = QVBoxLayout(self)
        self.cover_song_label = CoverSongLabel(self)
        self.song_time = SongTime(self)
        self.volume = Volume(self)
        self.previous_pause_next = PreviousPauseNext(self)
        self.shuffle_loop = ShuffleLoop(self)
        
        self.layout.addWidget(self.cover_song_label)
        self.layout.addWidget(self.song_time)
        self.layout.addWidget(self.volume)
        self.layout.addWidget(self.previous_pause_next)
        self.layout.addWidget(self.shuffle_loop)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Swappable Test")
    window.resize(900, 600)

    player_view = PlayerView()
    window.setCentralWidget(player_view)

    window.show()

    sys.exit(app.exec())
