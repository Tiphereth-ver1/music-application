from PySide6.QtWidgets import (QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit)
from PySide6.QtCore import (Slot, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)


class DownloaderWidget(QWidget):

    to_download_song = Signal(str)
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

        self.previewButton.setEnabled(True)
        self.downloadButton.setEnabled(False)

    @Slot(object)
    def allow_download(self, _info):
        self.downloadButton.setEnabled(True)

    def invalidate_preview(self):
        self.downloadButton.setEnabled(False)

    def download_song(self):
        self.to_download_song.emit(self.downloader_lineEdit.text())

    def preview_song(self):
        self.to_preview_song.emit(self.downloader_lineEdit.text())
        print("preview passed")

