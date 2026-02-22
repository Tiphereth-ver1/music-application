from pathlib import Path
from PySide6.QtCore import QFileSystemWatcher, QObject
from PySide6.QtWidgets import QApplication
import os
THEME_DIR = Path(__file__).parent / "themes"

modes = ["dark", "light"]
qss_len = len(".qss")

class ThemeManager(QObject):
    def __init__(self, app : QApplication, theme_watcher : QFileSystemWatcher, parent = None):
        super().__init__(parent)
        self.app = app
        self.mode : str = ""
        self.current_theme = None
        self.theme_watcher = theme_watcher
        self.themes : dict = {}
        self.find_all_themes()

    def set_theme(self, theme: str) -> str:
        path = THEME_DIR / f"{self.themes[theme]}.qss"
        self.current_theme = theme
        self.theme_watcher.addPath(str(path))
        text = path.read_text(encoding="utf-8")
        self.app.setStyleSheet(text)

    def get_str_path(self, name: str) -> str:
        path = THEME_DIR / f"{name}.qss"
        return path

    def reload_theme(self, changed_path):
        if not os.path.exists(changed_path):
            return
        print(self.current_theme)
        self.set_theme(self.current_theme)
        print("theme reloaded")

        if changed_path not in self.theme_watcher.files():
            self.theme_watcher.addPath(changed_path)

    def find_all_themes(self):
        with os.scandir(THEME_DIR) as entries:
            for entry in entries:
                theme_dir = entry.name[:-qss_len]
                formatted = theme_dir.replace("_", " ").title()
                self.themes[formatted] = theme_dir
        print(self.themes)