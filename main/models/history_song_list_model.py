from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QPixmap, QIcon
from ..player import Player

class HistorySongListModel(QAbstractListModel):
    def __init__(self, player: Player, songs=None):
        super().__init__()
        self.player = player
        self._songs = list(player.history)
        self._icons = {}



        player.history_appended.connect(self.prepend_song)
        player.history_removed.connect(self.pop_front_song)
        player.history_modified.connect(self.sync_songs)

    def sync_songs(self):
        self.beginResetModel()
        self._songs = list(self.player.history)
        self.endResetModel()



    def rowCount(self, parent=None):
        # Return how many items are in the model
        return len(self._songs)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        song = self._songs[index.row()]

        if role == Qt.DisplayRole:
            return f"{song.get_info('title')} - {song.get_info('artist')}"
        if role == Qt.DecorationRole:
            if song not in self._icons:
                pixmap = QPixmap()
                pixmap.loadFromData(song.get_art())
                pixmap = pixmap.scaled(
                    40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self._icons[song] = QIcon(pixmap)
            return self._icons[song]
        return None
    
    def append_song(self, song):
        row = len(self._songs)
        self.beginInsertRows(QModelIndex(), row, row)
        self._songs.append(song)
        self.endInsertRows()
    
    def prepend_song(self, song):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._songs.insert(0,song)
        self.endInsertRows()
    
    def insert_song(self, idx, song):
        row = len(self._songs)
        if idx < row:
            self.beginInsertRows(QModelIndex(), idx, idx)
            self._songs.insert(idx,song)
            self.endInsertRows()

    def pop_front_song(self):
        self.beginRemoveRows(QModelIndex(), 0, 0)
        self._songs.pop(0)
        self.endRemoveRows()
    
    def pop_song(self):
        row = len(self._songs) - 1
        self.beginRemoveRows(QModelIndex(), row, row)
        self._songs.pop()
        self.endRemoveRows()

    def remove_song(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._songs.pop(row)
        self.endRemoveRows()
