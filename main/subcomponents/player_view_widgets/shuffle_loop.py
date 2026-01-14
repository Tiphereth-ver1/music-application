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

class ShuffleLoop(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(u"widget_4")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.setMinimumSize(QSize(500, 60))
        self.layout = QHBoxLayout(self)
        self.layout.setObjectName(u"layout")
        self.loopButton = QPushButton(self)
        self.loopButton.setObjectName(u"loopButton")
        self.loopButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layout.addWidget(self.loopButton)

        self.shuffleButton = QPushButton(self)
        self.shuffleButton.setObjectName(u"shuffleButton")
        self.shuffleButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layout.addWidget(self.shuffleButton)

        self.loopButton.setText("Loop")
        self.shuffleButton.setText("Shuffle")

