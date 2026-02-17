from PySide6.QtCore import (QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtGui import (QPixmap, QFont)

from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget, QPushButton, QListView, QDialog)

class CoverTitleBox(QWidget):
    def __init__(self, coverLabel, titleLabel, parent = None):
        super().__init__(parent)

        self.text_font = QFont()
        self.text_font.setPointSize(12)

        self.cover_title_box = QWidget(self)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMinimumSize(QSize(600, 250))
        self.internal_layout = QHBoxLayout(self.cover_title_box)
        self.cover_Label = QLabel(self.cover_title_box)
        self.cover_Label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.cover_Label.setMinimumSize(QSize(200, 200))
        self.cover_Label.setFont(self.text_font)
        self.title_Label = QLabel(self.cover_title_box)
        self.title_Label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.title_Label.setMinimumSize(QSize(0, 200))
        self.title_Label.setFont(self.text_font)

        self.internal_layout.addWidget(coverLabel)
        self.internal_layout.addWidget(titleLabel,alignment=Qt.AlignBottom)