from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Qt, QRect, QSize, QEvent, Signal
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from ...library_manager import PlaylistMeta
TITLE_ROLE = Qt.UserRole + 1
TIME_ROLE = Qt.UserRole + 2

PLAY_RECT = QRect(14, 14, 30, 30)

PLAY_RECT2 = QRect(44, 14, 30, 30)

class SongItemDelegate(QStyledItemDelegate):
    song_pressed = Signal(int, str)
    to_modify_song = Signal(str, int)
    def paint(self, painter, option, index):
        painter.save()

        # Selection background
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        icon1, icon2, icon3 = self._icon_rects(option)

        painter.fillRect(icon1, QColor(150, 150, 255))
        painter.fillRect(icon2, QColor(255, 150, 150))
        painter.fillRect(icon3, QColor(150, 255, 150))

        # Text
        painter.drawText(
            option.rect.adjusted(80, 0, 0, 0),
            Qt.AlignLeft | Qt.AlignVCenter,
            index.data(TITLE_ROLE)

        )

        painter.drawText(
            option.rect.adjusted(0, 0, -54, 0),
            Qt.AlignRight | Qt.AlignVCenter,
            index.data(TIME_ROLE)

        )

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(0, 48)
    
    def _icon_rects(self, option):
        rect = option.rect
        h = rect.height() - 28
        y = rect.top() + 14

        return (
            QRect(rect.left() + 14, y, 20, h),
            QRect(rect.left() + 44, y, 20, h),
            QRect(rect.right() - 34, y, 20, h),
        )


    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease:
            rect = option.rect
            pos = event.pos()  # already in viewport coordinates

            icon1, icon2, icon3 = self._icon_rects(option)

            if icon1.contains(pos):
                self.song_pressed.emit(index.row(), "play")
                return True

            if icon2.contains(pos):
                self.song_pressed.emit(index.row(), "queue")
                return True

            if icon3.contains(pos):
                self.to_modify_song.emit("single", index.row())
                return True

        return False

from ...library_manager import LibraryService, PlaylistMeta

class SongSerachListModel(QAbstractListModel):
    def __init__(self, library: LibraryService):
        super().__init__()
        self.lib = library
        self._song_ids : list[int] = []
    
    def update_song_ids(self, song_ids : list[int]):
        self.beginResetModel()
        self._song_ids = song_ids
        self.endResetModel()

    def rowCount(self, parent=None):
        # Return how many items are in the model
        return len(self._song_ids)
    
    def _to_time(self, length) -> str:
        length = round(length)
        minutes = length // 60
        seconds = length % 60
        return f"{minutes}:{seconds:02d}"


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        song_id = self._song_ids[index.row()]
        meta = self.lib.get_song_meta(song_id)

        if role == TITLE_ROLE:
            return f"{meta.title} - {meta.artist}"
        if role == TIME_ROLE:
            return self._to_time(meta.duration)
        return None