import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot, QTimer
from PySide6.QtGui import (QPixmap)
from pathlib import Path

from .ui_mainwindow import Ui_MainWindow
from .audio_engine import AudioEngine
from .song import Song
from . import Player, LoopMode

LOOP_MODES = [LoopMode.NONE, LoopMode.PLAYLIST, LoopMode.SINGLE]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)  # Ensure window is large enough for the layout

        # --- Audio engine ---
        self.engine = AudioEngine()
        self.player = self.engine.player

        songs = self.filepath_to_songs()
        # self.player._queue_songs(songs)
        # self.player._begin_playback()
        # self.engine.play_current()



        # --- Setup UI ---
        self.ui = Ui_MainWindow(self.player)
        # Attach the generated UI stack to this MainWindow so it is visible
        self.setCentralWidget(self.ui)
        self.swappable = self.ui.swappable
        self.navigation_bar = self.ui.leftbar
        self.rightbar = self.ui.rightbar
        self.queue_history_display = self.rightbar
        self.album_view = self.swappable.album_view
        self.player_view = self.swappable.player_view
        self.button_group = self.navigation_bar.button_group

        self.song_cover_label = self.player_view.cover_song_label

        self.nextButton = self.player_view.previous_pause_next.nextButton
        self.previousButton = self.player_view.previous_pause_next.previousButton
        self.pauseButton = self.player_view.previous_pause_next.pauseButton
        self.shuffleButton = self.player_view.shuffle_loop.shuffleButton
        self.loopButton = self.player_view.shuffle_loop.loopButton

        # --- Button wiring ---
        '''
        The way connect function works requires a Signal from a QObject or objects in Qt.
        How does it work? By finding an event (Signals from QObjects emitted as a signal),
        you can perform a function by passing in the object form of the function to be called.
        '''

        self.nextButton.clicked.connect(self.next_song)
        self.previousButton.clicked.connect(self.previous_song)
        self.pauseButton.clicked.connect(self.pause)
        self.shuffleButton.clicked.connect(self.shuffle)
        self.loopButton.clicked.connect(self.loop)
        self.button_group.idClicked.connect(self.swappable.stack.setCurrentIndex)

        # --- Update queue/history when the player signals changes ---
        # self.player.queue_appended.connect(self.queue_history_display.append_queue)
        # self.player.queue_removed.connect(self.queue_history_display.pop_queue)
        # self.player.queue_looped.connect(self.queue_history_display.loop_queue)
        # self.player.history_appended.connect(self.queue_history_display.append_history)
        # self.player.history_removed.connect(self.queue_history_display.pop_history)
        self.engine.song_ended.connect(self.next_song)
        self.ui.returning_song.connect(self.receive_song)
        self.ui.clearing_history.connect(self.clear_history)
        self.ui.clearing_queue.connect(self.clear_queue)
        self.ui.updating_view.connect(self.refresh_song_list)

        # --- Timer for updating song progress ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.player_view.song_time.update_progress(
            self.engine.get_time(),
            self.engine.get_song_length()
        ))
        self.timer.start(500)  # update twice per second

        # --- Initialize displays ---
        # self.song_cover_label.update_now_playing(self.player.get_playing())
        # self.queue_history_display.update_queue(self.player.queue)
        # self.queue_history_display.update_history(self.player.history)
        self.album_view.set_songs(songs)

    def filepath_to_songs(self):
        base_dir = Path(__file__).resolve().parent.parent
        music_folder = base_dir / "music"
        songs = []
        for file_path in music_folder.rglob("*.mp3"):
            rel_path = file_path.relative_to(base_dir)
            songs.append(Song(rel_path))
        return songs

    @Slot()
    def refresh_song_list(self):
        songs = self.filepath_to_songs()
        self.album_view.set_songs(songs)
        print("song list refreshed")


    
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
    def clear_queue(self):
        print("queue cleared")
        self.player.clear_queue()

    @Slot()
    def clear_history(self):
        print("history cleared")
        self.player.clear_history()


    @Slot()
    def receive_song(self,song,mode):
        if mode == "queue":
            self.queue_song(song)
        elif mode == "play":
            self.player.play_now(song)
            self.engine.play_current()
            self.song_cover_label.update_now_playing(self.engine.player.get_playing())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


