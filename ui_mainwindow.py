# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled2.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1084, 648)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(250, 0, 520, 640))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QSize(500, 280))
        self.coverLabel = QLabel(self.groupBox_3)
        self.coverLabel.setObjectName(u"coverLabel")
        self.coverLabel.setGeometry(QRect(110, 10, 250, 250))
        self.coverLabel.setMinimumSize(QSize(250, 250))
        self.coverLabel.setPixmap(QPixmap())

        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.groupBox_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy2)
        self.groupBox_6.setMinimumSize(QSize(500, 50))
        self.horizontalLayout = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.song_label = QLabel(self.groupBox_6)
        self.song_label.setObjectName(u"song_label")
        sizePolicy1.setHeightForWidth(self.song_label.sizePolicy().hasHeightForWidth())
        self.song_label.setSizePolicy(sizePolicy1)
        self.song_label.setMinimumSize(QSize(200, 30))

        self.horizontalLayout.addWidget(self.song_label)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.groupBox = QGroupBox(self.groupBox_2)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.groupBox.setMinimumSize(QSize(500, 60))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy2.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy2.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.pushButton_3)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)
        self.pushButton.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_5 = QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy2.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy2)
        self.groupBox_5.setMinimumSize(QSize(500, 60))
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_4 = QPushButton(self.groupBox_5)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy2.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.groupBox_5)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy2.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.pushButton_5)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.groupBox_4 = QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy2.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy2)
        self.groupBox_4.setMinimumSize(QSize(500, 100))
        self.progressBar = QProgressBar(self.groupBox_4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(50, 40, 421, 23))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.groupBox_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1084, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def reload_image(self, art_bytes):
        pixmap = QPixmap()
        if art_bytes:
            pixmap.loadFromData(art_bytes)
        else:
            pixmap = QPixmap(311, 301)  # blank placeholder
            pixmap.fill(Qt.gray)
        self.coverLabel.setPixmap(pixmap)
    
    def update_progress(self, song_time, song_length):
        print(int(100*song_time/song_length))
        self.progressBar.setValue(int(100*song_time/song_length))

    def int_to_time(length) -> str:
        minutes = length // 60
        seconds = length % 60
        return f"{minutes}:{seconds}"


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.song_label.setText(QCoreApplication.translate("MainWindow", u"song_label", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Shuffle", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
    # retranslateUi

