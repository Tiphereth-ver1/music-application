from PySide6.QtCore import (QSize)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget)

class ShuffleLoop(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(u"widget_4")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.setMinimumSize(QSize(500, 60))
        self.internal_layout = QHBoxLayout(self)
        self.internal_layout.setObjectName(u"layout")
        self.loopButton = QPushButton(self)
        self.loopButton.setObjectName(u"loopButton")
        self.loopButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.internal_layout.addWidget(self.loopButton)

        self.shuffleButton = QPushButton(self)
        self.shuffleButton.setObjectName(u"shuffleButton")
        self.shuffleButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.internal_layout.addWidget(self.shuffleButton)

        self.loopButton.setText("Loop")
        self.shuffleButton.setText("Shuffle")