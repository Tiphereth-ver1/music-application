from .song_downloader_tools import DownloadManager, DownloaderWidget, InfoWidget, VideoPreviewWidget
from PySide6.QtWidgets import (QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit)
from PySide6.QtCore import (Slot, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)


class DownloaderView(QWidget):
    updating_view = Signal()
    update_preview = Signal(dict)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.download_manager = DownloadManager(self)
        self.download_manager.updating_view.connect(self.update_view)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.internal_layout = QVBoxLayout(self)

        self.preview_widget = VideoPreviewWidget(self)
        self.internal_layout.addWidget(self.preview_widget)
        self.downloader_widget = DownloaderWidget(self)
        self.internal_layout.addWidget(self.downloader_widget)

        self.info_widget = InfoWidget(self)
        self.internal_layout.addWidget(self.info_widget)

        self.internal_layout.addStretch(1)
        self.download_manager.download_status.connect(self.update_status)
        self.downloader_widget.to_download_song.connect(self.download_manager.request_enqueue)
        self.downloader_widget.to_preview_song.connect(self.download_manager.preview_song)
        self.download_manager.return_preview.connect(self.preview_widget.update_preview)
        self.download_manager.return_preview.connect(self.downloader_widget.allow_download)

    
    
    def update_status(self, infos : dict):
        for info in self.info_widget.info_boxes.keys():
            print(infos[info])
            self.info_widget.info_boxes[info].setText(str(infos[info]))
        print("updated status")
    
    @Slot()
    def update_view(self):
        self.updating_view.emit()



