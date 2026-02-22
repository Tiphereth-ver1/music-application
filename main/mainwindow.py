import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot, QTimer
from PySide6.QtGui import (QPixmap, QPalette, QColor)
from pathlib import Path
from .song_subclasses import M4ASong, MP3Song, FLACSong

from .ui_mainwindow import Ui_MainWindow
from .audio_engine import AudioEngine
from .song import Song
from .library_manager import LibraryService
from . import Player, LoopMode, resources_rc, ThemeManager

LOOP_MODES = [LoopMode.NONE, LoopMode.PLAYLIST, LoopMode.SINGLE]

from dataclasses import dataclass

@dataclass(slots=True)
class AppContext:
    lib: LibraryService
    player: Player
    engine: AudioEngine
    theme_manager: ThemeManager


class MainWindow(QMainWindow):
    def __init__(self, ctx : AppContext):
        super().__init__()
        self.resize(1200, 700)  # Ensure window is large enough for the layout

        # --- Audio engine ---
        self.lib = ctx.lib
        self.player = ctx.player
        self.engine = ctx.engine
        self.theme_manager = ctx.theme_manager

        # --- Setup UI ---
        self.ui = Ui_MainWindow(self.lib, self.player, self.theme_manager, self)
        # Attach the generated UI stack to this MainWindow so it is visible
        self.setCentralWidget(self.ui)
        self.swappable = self.ui.swappable
        self.navigation_bar = self.ui.leftbar
        self.rightbar = self.ui.rightbar
        self.queue_history_display = self.rightbar
        self.album_view = self.swappable.album_view
        self.player_view = self.swappable.player_view
        self.button_group = self.navigation_bar.button_group
        self.cases = {
            "shuffle" : self.shuffle,
            "previous" : self.previous_song,
            "pause" : self.pause,
            "next" : self.next_song,
            "loop" : self.loop
        }

        self.song_cover_label = self.player_view.cover_song_label

        # --- Button wiring ---
        '''
        The way connect function works requires a Signal from a QObject or objects in Qt.
        How does it work? By finding an event (Signals from QObjects emitted as a signal),
        you can perform a function by passing in the object form of the function to be called.
        '''
        self.button_group.idClicked.connect(self.swappable.stack.setCurrentIndex)
        # --- Update queue/history when the player signals changes ---
        self.engine.song_ended.connect(self.next_song)
        self.ui.returning_song.connect(self.receive_song)
        self.ui.clearing_history.connect(self.clear_history)
        self.ui.clearing_queue.connect(self.clear_queue)
        self.ui.updating_view.connect(self.refresh_song_list)
        self.ui.perform_action.connect(self.perform_player_action)

        # --- Timer for updating song progress ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.player_view.song_time.update_progress(
            self.engine.get_time(),
            self.engine.get_song_length()
        ))
        self.timer.start(500)  # update twice per second

    @Slot(str)
    def perform_player_action(self, action: str):
        """Lookup the action in the cases dict and execute it."""
        func = self.cases.get(action)
        if func:
            func()
        else:
            logging.warning(f"[Warning] Unknown player action: {action}")
        
    @Slot()
    def refresh_song_list(self):
        songs = self.filepath_to_songs()
        self.album_view.set_songs(songs)

    def stop_playing(self):
        self.player._stop_playing()
    
    @Slot()
    def next_song(self):
        self.engine.player.next_song()
        self.engine.play_current()
        self.song_cover_label.update_now_playing(self.engine.player.get_playing())

    @Slot()
    def previous_song(self):
        self.engine.player.previous_song()
        self.engine.play_current()
        self.song_cover_label.update_now_playing(self.engine.player.get_playing())

    @Slot()
    def pause(self):
        self.engine.pause()
    
    @Slot()
    def shuffle(self):
        self.player.shuffle_queue()
    
    @Slot()
    def loop(self):
        self.player.toggle_loop(LOOP_MODES[(LOOP_MODES.index(self.player.loop_mode)+1)%3])
        print(self.player.loop_mode)
    
    @Slot()
    def queue_song(self, song):
        self.player._queue_song_back(song)
        print(f"{song.get_info('title')} queued")
    
    @Slot()
    def queue_songs(self, song):
        self.player._queue_songs(song)
        print(f"many songs queued")

    
    @Slot()
    def clear_queue(self):
        print("queue cleared")
        self.player.clear_queue()

    @Slot()
    def clear_history(self):
        print("history cleared")
        self.player.clear_history()


    @Slot()
    def receive_song(self,songs,mode):
        if mode == "queue":
            self.queue_songs(songs)
        elif mode == "play":
            self.clear_queue()
            self.stop_playing()
            self.player._queue_songs_front(songs)
            self.player._begin_playback()
            self.engine.play_current()
            self.song_cover_label.update_now_playing(self.player.get_playing())


if __name__ == "__main__":
    from PySide6.QtCore import QFileSystemWatcher
    import time, logging, os

    logging.basicConfig(level=logging.DEBUG) # Sets the threshold to DEBUG
    pre_startup = round(time.time()*1000)
    lib = LibraryService("music.db")
    engine = AudioEngine(lib)
    player = engine.player

    app = QApplication(sys.argv)
    app.theme_watcher = QFileSystemWatcher()

    theme = "Suika Kaiju"

    app.theme_watcher = QFileSystemWatcher()
    theme_manager = ThemeManager(app, app.theme_watcher)
    theme_manager.set_theme(theme)
    app.theme_watcher.fileChanged.connect(theme_manager.reload_theme)
    ctx = AppContext(
    lib=lib,
    player=player,
    engine=engine,
    theme_manager=theme_manager,
)

    pre_window = round(time.time()*1000)
    window = MainWindow(ctx)
    window.setWindowTitle("Ringo Music")
    window.show()
    startup = round(time.time()*1000)
    logging.debug(f"Window loading time : {startup - pre_window}")
    logging.debug(f"Application startup time : {startup - pre_startup}")
    sys.exit(app.exec())


