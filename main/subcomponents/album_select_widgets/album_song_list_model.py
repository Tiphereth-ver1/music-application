from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Qt, QRect, QSize, QEvent, Signal
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from ..album_grid_view_components import Album

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

        # Album art
        # icon = index.data(Qt.DecorationRole)
        # if icon:
        #     icon.paint(painter, option.rect.adjusted(4, 4, -4, -4), Qt.AlignLeft)


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

from ...song import Song

class AlbumSongListModel(QAbstractListModel):
    def __init__(self, album: Album):
        super().__init__()
        self._songs = list(album.get_songs())

    def rowCount(self, parent=None):
        # Return how many items are in the model
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