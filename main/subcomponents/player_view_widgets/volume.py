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

class Volume(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(u"widget_8")
        self.setMinimumSize(QSize(500, 50))
        self.horizontalLayout_4 = QHBoxLayout(self)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.minimum_volume = QLabel(self)
        self.minimum_volume.setObjectName(u"minimum_volume")
        self.minimum_volume.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.minimum_volume.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.minimum_volume)

        self.volumeSlider = QSlider(self)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.volumeSlider)

        self.maximum_volume = QLabel(self)
        self.maximum_volume.setObjectName(u"maximum_volume")
        self.maximum_volume.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.maximum_volume.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.maximum_volume)