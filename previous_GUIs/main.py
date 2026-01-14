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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1114, 699)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_5 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widget_5 = QWidget(self.centralwidget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_5.addWidget(self.widget_5)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setMinimumSize(QSize(520, 640))
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_10 = QWidget(self.widget_2)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setMinimumSize(QSize(500, 300))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.widget = QWidget(self.widget_10)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.widget.setMinimumSize(QSize(250, 250))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.coverLabel = QLabel(self.widget)
        self.coverLabel.setObjectName(u"coverLabel")
        sizePolicy2.setHeightForWidth(self.coverLabel.sizePolicy().hasHeightForWidth())
        self.coverLabel.setSizePolicy(sizePolicy2)
        self.coverLabel.setMinimumSize(QSize(250, 250))
        self.coverLabel.setScaledContents(False)

        self.verticalLayout.addWidget(self.coverLabel)


        self.horizontalLayout_3.addWidget(self.widget)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.widget_10)

        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy2.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy2)
        self.widget_3.setMinimumSize(QSize(500, 0))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.song_label = QLabel(self.widget_3)
        self.song_label.setObjectName(u"song_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.song_label.sizePolicy().hasHeightForWidth())
        self.song_label.setSizePolicy(sizePolicy3)
        self.song_label.setMinimumSize(QSize(200, 30))

        self.horizontalLayout_2.addWidget(self.song_label)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.widget_7 = QWidget(self.widget_2)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMinimumSize(QSize(500, 50))
        self.horizontalLayout = QHBoxLayout(self.widget_7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.song_time = QLabel(self.widget_7)
        self.song_time.setObjectName(u"song_time")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.song_time.sizePolicy().hasHeightForWidth())
        self.song_time.setSizePolicy(sizePolicy4)
        self.song_time.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.song_time)

        self.progressBar = QProgressBar(self.widget_7)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy5)
        self.progressBar.setMinimumSize(QSize(200, 0))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.song_finish_time = QLabel(self.widget_7)
        self.song_finish_time.setObjectName(u"song_finish_time")
        sizePolicy3.setHeightForWidth(self.song_finish_time.sizePolicy().hasHeightForWidth())
        self.song_finish_time.setSizePolicy(sizePolicy3)
        self.song_finish_time.setMinimumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.song_finish_time)


        self.verticalLayout_2.addWidget(self.widget_7)

        self.widget_8 = QWidget(self.widget_2)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setMinimumSize(QSize(500, 50))
        self.horizontalLayout_4 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.minimum_volume = QLabel(self.widget_8)
        self.minimum_volume.setObjectName(u"minimum_volume")
        sizePolicy3.setHeightForWidth(self.minimum_volume.sizePolicy().hasHeightForWidth())
        self.minimum_volume.setSizePolicy(sizePolicy3)
        self.minimum_volume.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.minimum_volume)

        self.volumeSlider = QSlider(self.widget_8)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.volumeSlider)

        self.maximum_volume = QLabel(self.widget_8)
        self.maximum_volume.setObjectName(u"maximum_volume")
        sizePolicy3.setHeightForWidth(self.maximum_volume.sizePolicy().hasHeightForWidth())
        self.maximum_volume.setSizePolicy(sizePolicy3)
        self.maximum_volume.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.maximum_volume)


        self.verticalLayout_2.addWidget(self.widget_8)

        self.widget_6 = QWidget(self.widget_2)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy3.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy3)
        self.widget_6.setMinimumSize(QSize(500, 60))
        self.horizontalLayout_7 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.previousButton = QPushButton(self.widget_6)
        self.previousButton.setObjectName(u"previousButton")
        sizePolicy2.setHeightForWidth(self.previousButton.sizePolicy().hasHeightForWidth())
        self.previousButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.previousButton)

        self.pauseButton = QPushButton(self.widget_6)
        self.pauseButton.setObjectName(u"pauseButton")
        sizePolicy2.setHeightForWidth(self.pauseButton.sizePolicy().hasHeightForWidth())
        self.pauseButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.pauseButton)

        self.nextButton = QPushButton(self.widget_6)
        self.nextButton.setObjectName(u"nextButton")
        sizePolicy2.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy2)
        self.nextButton.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_7.addWidget(self.nextButton)


        self.verticalLayout_2.addWidget(self.widget_6)

        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy3.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy3)
        self.widget_4.setMinimumSize(QSize(500, 60))
        self.horizontalLayout_6 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.loopButton = QPushButton(self.widget_4)
        self.loopButton.setObjectName(u"loopButton")
        sizePolicy2.setHeightForWidth(self.loopButton.sizePolicy().hasHeightForWidth())
        self.loopButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.loopButton)

        self.pushButton_4 = QPushButton(self.widget_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy2.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.pushButton_4)


        self.verticalLayout_2.addWidget(self.widget_4)


        self.horizontalLayout_5.addWidget(self.widget_2)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy6)
        self.tabWidget.setMinimumSize(QSize(320, 0))
        self.tabWidget.setAutoFillBackground(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_11 = QWidget(self.tab)
        self.widget_11.setObjectName(u"widget_11")
        self.verticalLayout_4 = QVBoxLayout(self.widget_11)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.song_preview_3 = QWidget(self.widget_11)
        self.song_preview_3.setObjectName(u"song_preview_3")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.song_preview_3.sizePolicy().hasHeightForWidth())
        self.song_preview_3.setSizePolicy(sizePolicy7)
        self.song_preview_3.setMinimumSize(QSize(240, 60))
        self.horizontalLayout_10 = QHBoxLayout(self.song_preview_3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.title_label_3 = QLabel(self.song_preview_3)
        self.title_label_3.setObjectName(u"title_label_3")
        sizePolicy3.setHeightForWidth(self.title_label_3.sizePolicy().hasHeightForWidth())
        self.title_label_3.setSizePolicy(sizePolicy3)
        self.title_label_3.setMinimumSize(QSize(200, 30))

        self.horizontalLayout_10.addWidget(self.title_label_3)

        self.coverLabel_5 = QLabel(self.song_preview_3)
        self.coverLabel_5.setObjectName(u"coverLabel_5")
        sizePolicy2.setHeightForWidth(self.coverLabel_5.sizePolicy().hasHeightForWidth())
        self.coverLabel_5.setSizePolicy(sizePolicy2)
        self.coverLabel_5.setMinimumSize(QSize(50, 50))
        self.coverLabel_5.setScaledContents(False)

        self.horizontalLayout_10.addWidget(self.coverLabel_5)

        self.horizontalLayout_10.setStretch(1, 1)

        self.verticalLayout_4.addWidget(self.song_preview_3)

        self.song_preview_2 = QWidget(self.widget_11)
        self.song_preview_2.setObjectName(u"song_preview_2")
        sizePolicy7.setHeightForWidth(self.song_preview_2.sizePolicy().hasHeightForWidth())
        self.song_preview_2.setSizePolicy(sizePolicy7)
        self.song_preview_2.setMinimumSize(QSize(240, 60))
        self.horizontalLayout_9 = QHBoxLayout(self.song_preview_2)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.title_label_2 = QLabel(self.song_preview_2)
        self.title_label_2.setObjectName(u"title_label_2")
        sizePolicy3.setHeightForWidth(self.title_label_2.sizePolicy().hasHeightForWidth())
        self.title_label_2.setSizePolicy(sizePolicy3)
        self.title_label_2.setMinimumSize(QSize(200, 30))

        self.horizontalLayout_9.addWidget(self.title_label_2)

        self.coverLabel_4 = QLabel(self.song_preview_2)
        self.coverLabel_4.setObjectName(u"coverLabel_4")
        sizePolicy2.setHeightForWidth(self.coverLabel_4.sizePolicy().hasHeightForWidth())
        self.coverLabel_4.setSizePolicy(sizePolicy2)
        self.coverLabel_4.setMinimumSize(QSize(50, 50))
        self.coverLabel_4.setScaledContents(False)

        self.horizontalLayout_9.addWidget(self.coverLabel_4)

        self.horizontalLayout_9.setStretch(1, 1)

        self.verticalLayout_4.addWidget(self.song_preview_2)

        self.song_preview = QWidget(self.widget_11)
        self.song_preview.setObjectName(u"song_preview")
        sizePolicy7.setHeightForWidth(self.song_preview.sizePolicy().hasHeightForWidth())
        self.song_preview.setSizePolicy(sizePolicy7)
        self.song_preview.setMinimumSize(QSize(240, 60))
        self.horizontalLayout_8 = QHBoxLayout(self.song_preview)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.title_label = QLabel(self.song_preview)
        self.title_label.setObjectName(u"title_label")
        sizePolicy3.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy3)
        self.title_label.setMinimumSize(QSize(200, 30))

        self.horizontalLayout_8.addWidget(self.title_label)

        self.coverLabel_3 = QLabel(self.song_preview)
        self.coverLabel_3.setObjectName(u"coverLabel_3")
        sizePolicy2.setHeightForWidth(self.coverLabel_3.sizePolicy().hasHeightForWidth())
        self.coverLabel_3.setSizePolicy(sizePolicy2)
        self.coverLabel_3.setMinimumSize(QSize(50, 50))
        self.coverLabel_3.setScaledContents(False)

        self.horizontalLayout_8.addWidget(self.coverLabel_3)

        self.horizontalLayout_8.setStretch(1, 1)

        self.verticalLayout_4.addWidget(self.song_preview, 0, Qt.AlignTop)


        self.verticalLayout_3.addWidget(self.widget_11)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1114, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.coverLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.song_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.song_time.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.song_finish_time.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.minimum_volume.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.maximum_volume.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.previousButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pauseButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.loopButton.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Shuffle", None))
        self.title_label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.coverLabel_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.coverLabel_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.coverLabel_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
    # retranslateUi

