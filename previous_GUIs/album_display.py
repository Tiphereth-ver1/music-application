# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'album_display.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar, QScrollArea,
    QVBoxLayout, QWidget)

from album_indexer import Album_Indexer
from album import Album


ROWS = 4
COLUMNS = 4

class Ui_MainWindow():
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)

        # --- Central widget ---
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.centralLayout = QVBoxLayout(self.centralwidget)

        # --- Main horizontal container ---
        self.widget_2 = QWidget()
        self.horizontalLayout = QHBoxLayout(self.widget_2)

        # --- Sidebar ---
        self.widget_3 = QWidget()
        self.widget_3.setFixedWidth(200)  # sidebar width
        self.horizontalLayout.addWidget(self.widget_3)

        # --- Scrollable album area ---
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.horizontalLayout.addWidget(self.scrollArea)  # take remaining space

        # --- Content inside scroll area ---
        self.widget = QWidget()
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(20)
        self.scrollArea.setWidget(self.widget)

        # --- Add main container to central layout ---
        self.centralLayout.addWidget(self.widget_2)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))

    def update_ui(self, albums: list[Album]):
        for album in albums:
            self.add_album(album)

    def add_album(self, album: Album):
        index = self.gridLayout.count()
        row = index // COLUMNS  # COLUMNS = 4
        col = index % COLUMNS

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())

        album_display = QWidget(self.widget)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(album_display.sizePolicy().hasHeightForWidth())
        album_display.setSizePolicy(sizePolicy1)
        album_display.setMinimumSize(200, 200)
        album_display.setMaximumSize(250, 250)
        album_display.setAutoFillBackground(False)

        
        verticalLayout = QVBoxLayout(album_display)
        verticalLayout.setObjectName(u"verticalLayout")
        verticalLayout.setContentsMargins(-1, -1, 9, -1)

        CoverLabel = QLabel(album_display)
        CoverLabel.setObjectName(u"CoverLabel")
        sizePolicy.setHeightForWidth(CoverLabel.sizePolicy().hasHeightForWidth())
        CoverLabel.setSizePolicy(sizePolicy)
        CoverLabel.setMinimumSize(QSize(150, 150))
        self.reload_preview(CoverLabel, album.get_cover())
        verticalLayout.addWidget(CoverLabel)

        title_label = QLabel(album_display)
        title_label.setText(album.info_check()[0])
        verticalLayout.addWidget(title_label)


        self.gridLayout.addWidget(album_display, row, col, alignment=Qt.AlignTop | Qt.AlignLeft)

    
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
    
    



if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow
    from song import Song
    from album_indexer import Album_Indexer

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)


    album_indexer = Album_Indexer()
    songs = album_indexer.filepath_to_songs()
    album_indexer.set_songs(songs)
    album_indexer.get_albums()
    ui.update_ui(album_indexer.get_albums())



    MainWindow.show()
    sys.exit(app.exec())
