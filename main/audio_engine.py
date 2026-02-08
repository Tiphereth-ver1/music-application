import vlc
from PySide6.QtCore import QObject, Signal
from .library_manager import LibraryService
from .player import Player

class AudioEngine(QObject):
    song_ended = Signal()

    def __init__(self, library : LibraryService):
        super().__init__()
        self.instance = vlc.Instance()
        self.lib = library
        self.vlc_player = self.instance.media_player_new()
        self.player = Player(library)
        self.event_manager = self.vlc_player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_song_finished)


    def play_current(self):
        song_id = self.player.get_playing()

        if not song_id:
            return
        abs_path: Path = self.lib.abs_song_path(song_id)
        media = self.instance.media_new(str(abs_path))
        self.vlc_player.set_media(media)
        self.vlc_player.play()


    def pause(self):
        self.vlc_player.pause()

    def stop(self):
        self.vlc_player.stop()
    
    def get_time(self):
        return self.vlc_player.get_time()//1000

    def get_song_length(self):
        return self.vlc_player.get_length()//1000
    
    def on_song_finished(self, event):
        self.song_ended.emit()  # Notify anyone listening via Qt signal
