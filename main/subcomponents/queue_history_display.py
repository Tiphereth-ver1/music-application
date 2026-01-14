from PySide6.QtCore import (Signal, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy, QScrollArea,
    QSlider, QSpacerItem, QStackedWidget, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget, QListView)

from ..models import QueueSongListModel, HistorySongListModel
from ..player import Player

class QueueHistoryDisplay(QWidget):
    clearing_queue = Signal()
    clearing_history = Signal()
    def __init__(self, player: Player, parent = None):
        super().__init__(parent)
        self.queue_widgets = []
        self.history_widgets = []

        '''
        Initialise tab Widget
        '''
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.tabWidget.setMinimumSize(QSize(320, 0))
        self.tabWidget.setAutoFillBackground(False)


        # --- Queue Tab ---
        '''
        Scroll areas are special QWidgets which can resize naturally to fit the area which they take. Key notes:
        - The scroll area needs a widget to attach to. Then you can add elements to the widget as you normally do.
        - The widget needs to be unconstrained (no parent to allow the scroll area to determine parameters for you)
        '''
        self.tab = QWidget()
        self.queue_tab_layout = QVBoxLayout(self.tab)
        self.queue_tab_layout.setObjectName(u"queue_tab_layout")

        self.queue_view = QListView()
        self.queue_model = QueueSongListModel(player)
        self.queue_view.setModel(self.queue_model)
        self.queue_view.setIconSize(QSize(40,40))  # must set icon size
        self.queue_tab_layout.addWidget(self.queue_view)

        self.clear_queue_button = QPushButton("Clear Queue")
        self.clear_queue_button.setFixedHeight(40)
        self.queue_tab_layout.addWidget(self.clear_queue_button)
        self.clear_queue_button.clicked.connect(self.clearing_queue.emit)




        # --- History Tab ---
        self.tab_2 = QWidget()
        self.history_tab_layout = QVBoxLayout(self.tab_2)
        self.history_tab_layout.setObjectName("history_tab_layout")

        self.history_view = QListView()
        self.history_model = HistorySongListModel(player)
        self.history_view.setModel(self.history_model)
        self.history_view.setIconSize(QSize(40,40))
        self.history_tab_layout.addWidget(self.history_view)

        self.clear_history_button = QPushButton("Clear History")
        self.clear_history_button.setFixedHeight(40)
        self.history_tab_layout.addWidget(self.clear_history_button)
        self.clear_history_button.clicked.connect(self.clearing_history.emit)

        '''
        Adding tabs to tab widget
        '''
        self.tabWidget.addTab(self.tab, "Queue")
        self.tabWidget.addTab(self.tab_2, "History")

        
        # At the end of __init__, after adding tabs
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tabWidget)
        self.setLayout(main_layout)



    def reload_preview(self, label: QLabel, art_bytes):
        if art_bytes:
            pixmap = QPixmap()
            pixmap.loadFromData(art_bytes)

            pixmap = pixmap.scaled(
                label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            pixmap = QPixmap(50, 50)
            pixmap.fill(Qt.gray)

        label.setPixmap(pixmap)
        