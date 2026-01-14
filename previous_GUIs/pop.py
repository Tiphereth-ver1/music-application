# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nono.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1060, 700)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(10, 10, 981, 618))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.widget_3)

        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(800, 600))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Album_Display = QWidget(self.widget)
        self.Album_Display.setObjectName(u"Album_Display")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Album_Display.sizePolicy().hasHeightForWidth())
        self.Album_Display.setSizePolicy(sizePolicy1)
        self.Album_Display.setMinimumSize(QSize(200, 200))
        self.Album_Display.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(self.Album_Display)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 9, -1)
        self.CoverLabel = QLabel(self.Album_Display)
        self.CoverLabel.setObjectName(u"CoverLabel")
        sizePolicy.setHeightForWidth(self.CoverLabel.sizePolicy().hasHeightForWidth())
        self.CoverLabel.setSizePolicy(sizePolicy)
        self.CoverLabel.setMinimumSize(QSize(150, 150))

        self.verticalLayout.addWidget(self.CoverLabel)

        self.label_2 = QLabel(self.Album_Display)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.gridLayout.addWidget(self.Album_Display, 0, 1, 1, 1)

        self.Album_Display_2 = QWidget(self.widget)
        self.Album_Display_2.setObjectName(u"Album_Display_2")
        sizePolicy1.setHeightForWidth(self.Album_Display_2.sizePolicy().hasHeightForWidth())
        self.Album_Display_2.setSizePolicy(sizePolicy1)
        self.Album_Display_2.setMinimumSize(QSize(200, 200))
        self.Album_Display_2.setAutoFillBackground(False)
        self.verticalLayout_2 = QVBoxLayout(self.Album_Display_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, 9, -1)
        self.CoverLabel_2 = QLabel(self.Album_Display_2)
        self.CoverLabel_2.setObjectName(u"CoverLabel_2")
        sizePolicy.setHeightForWidth(self.CoverLabel_2.sizePolicy().hasHeightForWidth())
        self.CoverLabel_2.setSizePolicy(sizePolicy)
        self.CoverLabel_2.setMinimumSize(QSize(150, 150))

        self.verticalLayout_2.addWidget(self.CoverLabel_2)

        self.label_3 = QLabel(self.Album_Display_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)


        self.gridLayout.addWidget(self.Album_Display_2, 0, 2, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 1)

        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1060, 21))
        self.menuMakomi = QMenu(self.menubar)
        self.menuMakomi.setObjectName(u"menuMakomi")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuMakomi.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.CoverLabel.setText(QCoreApplication.translate("MainWindow", u"CoverLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Album Name", None))
        self.CoverLabel_2.setText(QCoreApplication.translate("MainWindow", u"CoverLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Album Name", None))
        self.menuMakomi.setTitle(QCoreApplication.translate("MainWindow", u"Makomi", None))
    # retranslateUi

