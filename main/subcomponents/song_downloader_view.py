from .song_downloader_tools import DownloadManager, DownloaderWidget, InfoWidget, VideoPreviewWidget, DownloadItemDelegate, SongDownloadListModel, LINK_ROLE, ID_ROLE
from PySide6.QtWidgets import (QSizePolicy, QListView, QVBoxLayout, QWidget)
from PySide6.QtCore import (Slot, Signal, QModelIndex)
from ..library_manager import LibraryService


class DownloaderView(QWidget):
    updating_view = Signal()
    update_preview = Signal(dict)
    download_song = Signal(str, object, str)

    def __init__(self, library : LibraryService, parent = None):
        super().__init__(parent)
        self.download_manager = DownloadManager(library, self)
        self.download_manager.updating_view.connect(self.update_view)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.internal_layout = QVBoxLayout(self)

        self.preview_widget = VideoPreviewWidget(self)
        self.internal_layout.addWidget(self.preview_widget)
        self.downloader_widget = DownloaderWidget(self)
        self.internal_layout.addWidget(self.downloader_widget)

        self.info_widget = InfoWidget(self)
        self.internal_layout.addWidget(self.info_widget)

        self.songs_download_view = QListView()
        self.songs_download_view.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.songs_download_model = SongDownloadListModel()
        self.delegate = DownloadItemDelegate(self.songs_download_view)
        self.songs_download_view.setItemDelegate(self.delegate)
        self.songs_download_view.setModel(self.songs_download_model)
        self.delegate.item_pressed.connect(self.return_enqueue)
        self.internal_layout.addWidget(self.songs_download_view, 3)

        self.internal_layout.addStretch(1)
        self.download_manager.download_status.connect(self.update_status)
        self.downloader_widget.to_download_song.connect(self.download_manager.request_enqueue)
        self.download_song.connect(self.download_manager.request_enqueue)
        self.downloader_widget.to_preview_song.connect(self.download_manager.classify_input)
        self.download_manager.return_preview.connect(self.preview_widget.update_preview)
        self.download_manager.return_preview.connect(self.downloader_widget.allow_single_download)
        self.download_manager.return_playlist_preview.connect(self.songs_download_model.update_song_list)
        self.download_manager.return_playlist_preview.connect(self.downloader_widget.allow_playlist_download)

    #  Legacy code, remember 
    # @Slot(int)
    # def return_enqueue(self, idx : int) -> None:
    #     url, opt, video_id = self.songs_download_model.song_list[idx][1].get('Link'), self.downloader_widget.return_option(), self.songs_download_model.song_list[idx][0]
    #     self.download_song.emit(url, opt, video_id)

    @Slot(QModelIndex)
    def return_enqueue(self, idx: QModelIndex) -> None:
        url = idx.data(LINK_ROLE)
        video_id = idx.data(ID_ROLE)
        opt = self.downloader_widget.return_option()
        self.download_song.emit(url, opt, video_id)
        
    @Slot(dict)
    def update_status(self, infos : dict) -> None:
        for info in infos.keys():
            self.info_widget.info_boxes[info].setText(str(infos[info]))
    
    @Slot()
    def update_view(self):
        self.updating_view.emit()



