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

class PreviousPauseNext(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(u"widget_6")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.setMinimumSize(QSize(500, 60))
        self.layout = QHBoxLayout(self)
        self.previousButton = QPushButton(self)
        self.previousButton.setObjectName(u"previousButton")
        self.previousButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layout.addWidget(self.previousButton)

        self.pauseButton = QPushButton(self)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layout.addWidget(self.pauseButton)

        self.nextButton = QPushButton(self)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.nextButton.setMinimumSize(QSize(0, 0))

        self.layout.addWidget(self.nextButton)

        self.previousButton.setText("Previous")
        self.pauseButton.setText("Pause")
        self.nextButton.setText("Next")


