from PySide6.QtCore import (QSize, Qt, Signal)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget)

class ButtonBox(QWidget):
    edit_playlist = Signal()
    add_queue_playlist = Signal(str)
    set_playlist_to_add = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.internal_layout = QHBoxLayout(self)
        self.internal_layout.setObjectName(u"layout")

        self.playButton = QPushButton("Play", self)
        self.playButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.queueButton = QPushButton("Queue", self)
        self.queueButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.editButton = QPushButton("Edit", self)
        self.editButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.addButton = QPushButton("Add Songs", self)
        self.addButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.internal_layout.addWidget(self.playButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.internal_layout.addWidget(self.queueButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.internal_layout.addWidget(self.editButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.internal_layout.addWidget(self.addButton, alignment = Qt.AlignmentFlag.AlignLeft)

        self.playButton.clicked.connect(self.play_playlist)
        self.queueButton.clicked.connect(self.queue_playlist)
        self.editButton.clicked.connect(self.edit_playlist_pressed)
        self.addButton.clicked.connect(self.toggle_add_mode)

    def play_playlist(self):
        self.add_queue_playlist.emit("play")
    
    def queue_playlist(self):
        self.add_queue_playlist.emit("queue")
    
    def edit_playlist_pressed(self):
        print("Edit playlist")
        self.edit_playlist.emit()
    
    def toggle_add_mode(self):
        self.set_playlist_to_add.emit()