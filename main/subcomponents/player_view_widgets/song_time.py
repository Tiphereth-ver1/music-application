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

class SongTime(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(u"widget_7")
        self.setMinimumSize(QSize(500, 50))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.song_time = QLabel(self)
        self.song_time.setObjectName(u"song_time")
        self.song_time.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.song_time.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.song_time)

        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progressBar.setMinimumSize(QSize(200, 0))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.song_finish_time = QLabel(self)
        self.song_finish_time.setObjectName(u"song_finish_time")
        self.song_finish_time.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.song_finish_time.setMinimumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.song_finish_time)
    
    def update_progress(self, song_time, song_length):
        if song_length:
            percentage = int(100*song_time/song_length)
        else:
            percentage = 0
        self.progressBar.setValue(percentage)
        self.song_time.setText(self.int_to_time(song_time))
        self.song_finish_time.setText(self.int_to_time(song_length))

    def int_to_time(self, length) -> str:
        minutes = length // 60
        seconds = length % 60
        return f"{minutes}:{seconds:02d}"
