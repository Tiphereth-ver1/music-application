from PySide6.QtWidgets import (QSizePolicy, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QLabel)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QFont)

from enum import Enum
class INFO_BOX(Enum):
    Downloaded = "Downloaded"
    Total = "Total"  
    Percentage = "Percentage"
    Speed = "Speed"  
    ETA = "ETA"

class InfoWidget(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.layout = QHBoxLayout(self)
        self.info_boxes : dict = {}
        self.info_box_font = QFont()
        self.info_box_font.setPointSize(12)
        for info in INFO_BOX:
            self.create_info_box(info)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

    def create_info_box(self, selection : INFO_BOX):
        info_box = QFrame(self)
        info_box.setObjectName("Selector")
        info_box.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        info_box.setStyleSheet("""
            QWidget#Selector {
                border: 1px solid #444;
                border-radius: 6px;
            }
        """)

        info_box_layout = QVBoxLayout(info_box)
        upper_text = QLabel(selection.value, info_box, alignment = Qt.AlignCenter | Qt.AlignBottom )
        upper_text.setFont(self.info_box_font)
        info_box_layout.addWidget(upper_text)
        lower_text = QLabel("N/A%", info_box, alignment = Qt.AlignTop | Qt.AlignCenter)
        lower_text.setFont(self.info_box_font)
        info_box_layout.addWidget(lower_text)
        self.info_boxes[selection.value] = lower_text
        self.layout.addWidget(info_box)
        



