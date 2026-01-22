from PySide6.QtCore import (QSize, Qt, Signal)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget)

class ButtonBox(QWidget):
    add_queue_album = Signal(str)
    edit_album = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.internal_layout = QHBoxLayout(self)
        self.internal_layout.setObjectName(u"layout")

        self.playButton = QPushButton("Play", self)
        self.playButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.queueButton = QPushButton("Queue", self)
        self.queueButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.editButton = QPushButton("Edit", self)
        self.editButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.internal_layout.addWidget(self.playButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.internal_layout.addWidget(self.queueButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.internal_layout.addWidget(self.editButton, alignment = Qt.AlignmentFlag.AlignLeft)

        self.playButton.clicked.connect(self.play_album)
        self.queueButton.clicked.connect(self.queue_album)
        self.editButton.clicked.connect(self.edit_album_pressed)

    def play_album(self):
        self.add_queue_album.emit("play")
    
    def queue_album(self):
        self.add_queue_album.emit("queue")
    
    def edit_album_pressed(self):
        self.edit_album.emit("album")