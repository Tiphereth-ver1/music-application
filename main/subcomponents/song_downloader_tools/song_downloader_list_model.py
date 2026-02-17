from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Qt, QRect, QSize, QEvent, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyle

DOWNLOAD_ROLE = Qt.UserRole + 1

def colored_icon(path, color):
    pixmap = QPixmap(path)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)


class DownloadItemDelegate(QStyledItemDelegate):
    item_pressed = Signal(QModelIndex)

    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 48)

    def paint(self, painter, option, index):
        painter.save()
        try:
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())

            icon1 = self._icon_rect(option)
            icon1 = index.data(DOWNLOAD_ROLE)
            if icon and isinstance(icon, QIcon):
                icon.paint(painter, icon_rect, Qt.AlignCenter)


            painter.drawText(
                option.rect.adjusted(20, 0, 0, 0),
                Qt.AlignLeft | Qt.AlignVCenter,
                index.data(TITLE_ROLE) or ""
            )

            painter.drawText(
                option.rect.adjusted(0, 0, -54, 0),
                Qt.AlignRight | Qt.AlignVCenter,
                index.data(TIME_ROLE) or ""
            )
        finally:
            painter.restore()

    def _icon_rect(self, option) -> QRect:
        rect = option.rect
        h = rect.height() - 28
        y = rect.top() + 14
        return QRect(rect.right() - 34, y, 20, h)


    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease:
            pos = event.pos()
            icon1 = self._icon_rect(option)
            if icon1.contains(pos):
                self.item_pressed.emit(index)
                return True
        return False


TITLE_ROLE = Qt.UserRole + 1
TIME_ROLE  = Qt.UserRole + 2
LINK_ROLE  = Qt.UserRole + 3
ID_ROLE    = Qt.UserRole + 4

class SongDownloadListModel(QAbstractListModel):
    def __init__(self, parent = None):
        super().__init__()
        self.song_list = list()
    
    def update_song_list(self, info_dict: dict):
        self.beginResetModel()
        self.song_list = sorted(
            info_dict.items(),
            key=lambda kv: kv[1].get("Index", 10**9)
        )
        self.endResetModel()


    def rowCount(self, parent=None):
        return len(self.song_list)
    
    def _to_time(self, length) -> str:
        length = round(length)
        minutes = length // 60
        seconds = length % 60
        return f"{minutes}:{seconds:02d}"

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        video_id, info = self.song_list[index.row()]  # (id, dict)

        if role == TITLE_ROLE:
            return f"{info.get('Title')} - {info.get('Uploader')}"
        if role == TIME_ROLE:
            return self._to_time(info.get('Duration'))
        if role == DOWNLOAD_ROLE:
            return colored_icon(":/assets/icons/Downloader.svg", "white")
        return None
