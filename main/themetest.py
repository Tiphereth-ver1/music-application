from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class ThemePreview(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Label text"))

        layout.addWidget(QPushButton("Button"))
        tb = QToolButton(text="ToolButton")
        tb.setCheckable(True)
        layout.addWidget(tb)

        layout.addWidget(QLineEdit("Text input"))
        layout.addWidget(QSlider(Qt.Horizontal))

        tabs = QTabWidget()
        tabs.addTab(QLabel("Tab 1"), "Tab One")
        tabs.addTab(QLabel("Tab 2"), "Tab Two")
        layout.addWidget(tabs)
