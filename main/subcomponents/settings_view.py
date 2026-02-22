from PySide6.QtCore import (QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtWidgets import (QSizePolicy, QVBoxLayout, QWidget, QComboBox)
from ..theme_manager import ThemeManager

class SettingsView(QWidget):
    def __init__(self, theme_manager : ThemeManager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(QSize(520, 640))
        self.layout = QVBoxLayout(self)
        self.theme_combo_box = QComboBox(self)
        self.themes = self.theme_manager.themes
        self.fill_combo_box()
        self.layout.addWidget(self.theme_combo_box)
        self.theme_combo_box.currentTextChanged.connect(self.update_theme)
        self.theme_combo_box.setCurrentText(self.theme_manager.current_theme)


    def fill_combo_box(self):
        for name in self.themes.keys():
            self.theme_combo_box.addItem(name)
    
    def update_theme(self, theme : str):
        print(theme)
        self.theme_manager.set_theme(theme)

