from PySide6.QtWidgets import (QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QComboBox)
from PySide6.QtCore import (Slot, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from enum import Enum
from .song_downloader import DL_OPTIONS

formats = {"MP3" : DL_OPTIONS.mp3, 
           "M4A" : DL_OPTIONS.m4a, 
           "FLAC" : DL_OPTIONS.flac}


class DownloaderWidget(QWidget):

    to_download_song = Signal(str, DL_OPTIONS)
    to_preview_song = Signal(str)
    preview_checked = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.layout = QHBoxLayout(self)

        self.downloader_label = QLabel("Youtube link:", self)
        self.layout.addWidget(self.downloader_label)

        self.downloader_lineEdit = QLineEdit(self)
        self.downloader_lineEdit.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.downloader_lineEdit.setMinimumWidth(200)
        self.downloader_lineEdit.textEdited.connect(self.invalidate_preview)
        self.layout.addWidget(self.downloader_lineEdit)

        self.previewButton = QPushButton("Preview", self)
        self.previewButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.previewButton.clicked.connect(self.preview_song)
        self.layout.addWidget(self.previewButton)

        self.downloadButton = QPushButton("Download", self)
        self.downloadButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.downloadButton.clicked.connect(self.download_song)
        self.layout.addWidget(self.downloadButton)

        self.formatComboBox = QComboBox(self)
        self.formatComboBox.addItems(formats.keys())
        self.formatComboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.formatComboBox.setMinimumWidth(80)
        self.layout.addWidget(self.formatComboBox)

        self.previewButton.setEnabled(True)
        self.downloadButton.setEnabled(False)

    @Slot(object)
    def allow_download(self, _info):
        self.downloadButton.setEnabled(True)

    def invalidate_preview(self):
        self.downloadButton.setEnabled(False)

    def download_song(self):
        self.to_download_song.emit(self.downloader_lineEdit.text(), formats[self.formatComboBox.currentText()])
        print(formats[self.formatComboBox.currentText()])

    def preview_song(self):
        self.to_preview_song.emit(self.downloader_lineEdit.text())
        print("preview passed")

