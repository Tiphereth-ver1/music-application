from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Qt, QRect, QSize, QEvent, Signal
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyle

TITLE_ROLE = Qt.UserRole + 1
TIME_ROLE = Qt.UserRole + 2


class SongDownloadListModel(QAbstractListModel):
    def __init__(self, parent = None):
        super().__init__()
        self._songs = list()

    def rowCount(self, parent=None):
        return len(self._songs)
    
    def _to_time(self, length) -> str:
        length = round(length)
        minutes = length // 60
        seconds = length % 60
        return f"{minutes}:{seconds:02d}"


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        song = self._songs[index.row()]

        if role == Qt.DisplayRole:
            return f"{song.get_info('title')} -> {self._to_time(song.get_song_length())}"
        if role == TITLE_ROLE:
            return song.get_info('title')
        if role == TIME_ROLE:
            return self._to_time(song.get_song_length())
        # if role == Qt.DecorationRole:
        #     pixmap = QPixmap(song.get_art())
        #     if pixmap.loadFromData(song.get_art()):
        #         # Optional: scale icon to a fixed size
        #         pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #         return QIcon(pixmap)
        return None  # fallback if no pixmap