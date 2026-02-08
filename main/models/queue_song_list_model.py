from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QPixmap, QIcon
from ..player import Player
from ..library_manager import LibraryService

class QueueSongListModel(QAbstractListModel):
    def __init__(self, player: Player, songs=None):
        super().__init__()
        self.player = player
        self.lib : LibraryService = player.lib
        self._songs = list(player.queue)
        self._icons_by_cover: dict[str, QIcon] = {}

        player.queue_appended.connect(self.prepend_song)
        player.queue_popped.connect(self.pop_front_song)
        player.queue_modified.connect(self.sync_songs)

    def _make_default_icon(self) -> QIcon:
        pm = QPixmap(40, 40)
        pm.fill(Qt.gray)
        return QIcon(pm)

    def sync_songs(self):
        self.beginResetModel()
        self._songs = list(self.player.queue)
        self.endResetModel()

    def rowCount(self, parent=None):
        # Return how many items are in the model
        return len(self._songs)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        song_id  = self._songs[index.row()]
        meta = self.lib.get_song_meta(song_id)

        if role == Qt.DisplayRole:
            return f"{meta.title} - {meta.artist}"
        if role == Qt.DecorationRole:
            if not meta.cover_path:
                return self._make_default_icon()

            # Cache key per album cover (shared by many songs)
            key = str(meta.cover_path)
            icon = self._icons_by_cover.get(key)
            if icon is not None:
                return icon

            cover_abs = str(meta.cover_path)

            pm = QPixmap(str(cover_abs))
            if pm.isNull():
                return self._make_default_icon()

            pm = pm.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon = QIcon(pm)
            self._icons_by_cover[key] = icon
            return icon
        return None
    
    def append_song(self, song_id):
        row = len(self._songs)
        self.beginInsertRows(QModelIndex(), row, row)
        self._songs.append(song_id)
        self.endInsertRows()
    
    def prepend_song(self, song_id):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._songs.insert(0,song_id)
        self.endInsertRows()
    
    def insert_song(self, idx, song_id):
        row = len(self._songs)
        if idx < row:
            self.beginInsertRows(QModelIndex(), idx, idx)
            self._songs.insert(idx,song_id)
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
