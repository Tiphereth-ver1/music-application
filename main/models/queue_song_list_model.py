from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QPixmap, QIcon
from ..player import Player
from ..library_manager import LibraryService

class QueueSongListModel(QAbstractListModel):
    def __init__(self, player: Player, songs=None):
        super().__init__()
        self.player = player
        self.lib : LibraryService = player.lib
        self._songs = player.queue
        self._icons_by_cover: dict[str, QIcon] = {}

        player.queue_prepended.connect(self.prepend_song)
        player.queue_appended.connect(self.prepend_song)
        player.queue_popped.connect(self.pop_front_song)
        player.queue_modified.connect(self.sync_songs)

    def _make_default_icon(self) -> QIcon:
        pm = QPixmap(40, 40)
        pm.fill(Qt.gray)
        return QIcon(pm)

    def sync_songs(self):
        self.beginResetModel()
        self._songs = self.player.queue
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
    
    def flags(self, index):
        f = super().flags(index)
        if index.isValid():
            return f | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
        else:
            # allow dropping onto empty area (append)
            return f | Qt.ItemIsDropEnabled

    def supportedDropActions(self):
        return Qt.MoveAction

    def moveRows(self, sourceParent, sourceRow, count, destinationParent, destinationChild):
        # sourceParent is the QObject of the source
        # sourceRow is the row number of the source
        # count is the number of objects to be moved
        # destinationParent is the QObject of the destination
        # destinationChild is the row number of the destination idk why
        print(sourceParent, sourceRow, count, destinationParent, destinationChild)
        print("moveRows", sourceRow, count, "->", destinationChild, "rowCount", self.rowCount())

        if count <= 0:
            return False
        if sourceParent != destinationParent:
            return False
        if destinationChild < 0:
            return False

        sourceLast = sourceRow + count - 1

        # Compute destination for beginMoveRows (PRE-move coordinates) 
        # this is specifically done to keep the 
        beginDest = destinationChild
        if destinationChild > sourceRow:
            beginDest = destinationChild + count
            print(beginDest)

        # Forbidden / no-op cases
        if beginDest == sourceRow or (sourceRow <= beginDest <= sourceLast + 1):
            return False

        self.beginMoveRows(sourceParent, sourceRow, sourceLast, destinationParent, beginDest)

        # ---- 2) Compute insertion index for Python list (POST-removal) ----
        insertRow = destinationChild
        if destinationChild > sourceRow:
            insertRow -= count

        block = self._songs[sourceRow:sourceRow + count]
        del self._songs[sourceRow:sourceRow + count]
        for i, item in enumerate(block):
            self._songs.insert(insertRow + i, item)

        self.endMoveRows()
        return True
    
    def append_song(self, song_id):
        row = len(self._songs)
        self.beginInsertRows(QModelIndex(), row, row)
        self.endInsertRows()
    
    def prepend_song(self, song_id):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.endInsertRows()
    
    def insert_song(self, idx, song_id):
        row = len(self._songs)
        if idx < row:
            self.beginInsertRows(QModelIndex(), idx, idx)
            self.endInsertRows()

    def pop_front_song(self):
        self.beginRemoveRows(QModelIndex(), 0, 0)
        self.endRemoveRows()
    
    def pop_song(self):
        row = len(self._songs) - 1
        self.beginRemoveRows(QModelIndex(), row, row)
        self.endRemoveRows()

    def remove_song(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self.endRemoveRows()