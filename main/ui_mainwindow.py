from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

from .swappable import Swappable
from .subcomponents import QueueHistoryDisplay, NavigationBar
from .player import Player

class Ui_MainWindow(QWidget):
    returning_song = Signal(object, str)
    updating_view = Signal()
    clearing_queue = Signal()
    clearing_history = Signal()
    def __init__(self, player: Player, parent = None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.leftbar = NavigationBar(self)
        self.leftbar.setMinimumSize(QSize(80, 600))
        self.leftbar.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)
        self.swappable = Swappable(self)
        self.swappable.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.swappable.setMinimumSize(QSize(450, 600))
        self.swappable.returning_song.connect(self.return_song)
        self.rightbar = QueueHistoryDisplay(player, self)
        self.rightbar.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.rightbar.setMinimumSize(QSize(250, 600))
        self.rightbar.clearing_history.connect(self.clear_history)
        self.rightbar.clearing_queue.connect(self.clear_queue)
        self.swappable.updating_view.connect(self.update_view)

        self.layout.addWidget(self.leftbar)
        self.layout.addWidget(self.swappable)
        self.layout.addWidget(self.rightbar)
        self.layout.setStretchFactor(self.swappable, 1)

    def return_song(self, song, mode):
        self.returning_song.emit(song, mode)
    
    def clear_queue(self):
        self.clearing_queue.emit()

    def clear_history(self):
        self.clearing_history.emit()
    
    def update_view(self):
        self.updating_view.emit()



