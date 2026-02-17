from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Qt, QRect, QSize, QEvent, Signal
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from ...library_manager import PlaylistMeta

TITLE_ROLE = Qt.UserRole + 1
TIME_ROLE = Qt.UserRole + 2
PLAY_ROLE = Qt.UserRole + 3
QUEUE_ROLE = Qt.UserRole + 4
DELETE_ROLE = Qt.UserRole + 5

def colored_icon(path, color):
    pixmap = QPixmap(path)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)


class SongItemDelegate(QStyledItemDelegate):
    song_pressed = Signal(int, str)
    to_delete_song = Signal(int)
    def paint(self, painter, option, index):
        painter.save()

        # Selection background
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Album art
        # icon = index.data(Qt.DecorationRole)
        # if icon:
        #     icon.paint(painter, option.rect.adjusted(4, 4, -4, -4), Qt.AlignLeft)


        icon1, icon2, icon3 = self._icon_rects(option)

        for icon_rect, role in zip((icon1, icon2, icon3), (PLAY_ROLE, QUEUE_ROLE, DELETE_ROLE)):
            icon = index.data(role)
            if icon and isinstance(icon, QIcon):
                icon.paint(painter, icon_rect, Qt.AlignCenter)

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
                self.to_delete_song.emit(index.row())
                return True

        return False

from ...library_manager import LibraryService, PlaylistMeta

class PlaylistSongListModel(QAbstractListModel):
    def __init__(self, library: LibraryService, playlist_meta: PlaylistMeta):
        super().__init__()
        self.lib = library
        self._song_ids = self.lib.get_songs_from_playlist(playlist_meta.id)

    def rowCount(self, parent=None):
        # Return how many items are in the model
        return len(self._song_ids)
    
    def _to_time(self, length) -> str:
        length = round(length)
        minutes = length // 60
        seconds = length % 60
        return f"{minutes}:{seconds:02d}"
    
    def remove_song(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._song_ids.pop(row)
        self.endRemoveRows()
 


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        song_id = self._song_ids[index.row()]
        meta = self.lib.get_song_meta(song_id)

        if role == PLAY_ROLE:
            return colored_icon(":/assets/icons/Play.svg", "white")
        if role == QUEUE_ROLE:
            return colored_icon(":/assets/icons/QueueLast.svg", "white")
        if role == DELETE_ROLE:
            return colored_icon(":/assets/icons/Close.svg", "white")
        if role == TITLE_ROLE:
            return meta.title
        if role == TIME_ROLE:
            return self._to_time(meta.duration)
        return None  # fallback if no pixmap