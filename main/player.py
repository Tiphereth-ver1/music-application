from .playlist import Playlist
from .song import Song
from collections import deque
from random import shuffle
import logging
logging.basicConfig(level=logging.DEBUG)
from PySide6.QtCore import QObject, Signal

from enum import Enum, auto

class LoopMode(Enum):
    NONE = "none"
    PLAYLIST = "playlist"
    SINGLE = "single"

class Player(QObject):
    queue_modified = Signal()
    history_modified = Signal()
    history_appended = Signal(Song)
    history_removed = Signal(Song)
    queue_appended = Signal(Song)
    queue_popped = Signal(Song)
    queue_appended_front = Signal(Song)
    '''
    To use a signal, define it outside of the initialisation. When in code, use self.function.emit()
    '''

    def __init__(self):
        super().__init__()
        self.playing = None
        self.queue : deque[Song] = deque()
        self.loop_mode : LoopMode = LoopMode.NONE
        self.history : list[Song] = []
        self.shuffle = False

    def _stop_playing(self):
        self.playing = None

    def _log_playing(self, song: Song):
        title, artist = song.get_info("title"), song.get_info("artist")
        logging.info(f"Playing {title} by {artist}")
    
    def _begin_playback(self):
        if not self.playing and self.queue:
            self._set_playing(self._advance_queue())

    def _push_history(self, song: Song) -> None:
        if song:
            self.history.append(song)
            self.history_appended.emit(song)
    
    def _pop_history(self) -> Song | None:
        if self.history:
            history = self.history.pop()
            self.history_removed.emit(history)
        else: 
            history = None
        return history
    
    def _set_playing(self, song: Song) -> None:
        self.playing = song
        if song:
            self._log_playing(song)
    
    def _can_advance(self) -> bool:
        '''
        Returns if 
        
        :param self: Description
        :return: Description
        :rtype: bool
        '''
        if not self.playing:
            return False
        if self.loop_mode == LoopMode.SINGLE:
            return True
        if self.queue:
            return True
        if self.loop_mode == LoopMode.PLAYLIST:
            return True
        return False
    

    def _advance_queue(self) -> Song | None:
        song = self.queue.popleft()
        if not song:
            return None
        
        self.queue_popped.emit(song)
        return song
        
    def _advance_playback(self) -> None:
        self._push_history(self.playing)

        if self.loop_mode == LoopMode.PLAYLIST:
            self._queue_song_back(self.playing)

        self._set_playing(self._advance_queue())


    def _queue_songs(self, songs : list[Song]) -> None:
        for song in songs:
            self._queue_song_back(song)
        # self.queue_modified.emit()
    
    def _queue_songs_front(self, songs : list[Song]) -> None:
        for song in reversed(songs):
            self._queue_song_front(song)
        self.queue_modified.emit()

    def _queue_song_back(self, song : Song) -> None:
        self.queue.append(song)
        self.queue_appended.emit(song)

    def _queue_song_front(self, song : Song) -> None:
        self.queue.appendleft(song)
        self.queue_appended_front.emit(song)
    
    def _queue_song_index(self, index : int, song : Song) -> None:
        tmp = list(self.queue)
        tmp.insert(index, song)
        self.queue = deque(tmp)
        self.queue_modified.emit()

    def get_playing(self) -> Song:
        return self.playing

    def toggle_loop(self, mode: LoopMode) -> None:
        self.loop_mode = mode
        logging.info(f"Set loop mode to {mode}")

    def play_now(self,song):
        self.clear_queue()
        self._push_history(self.playing)
        self._set_playing(song)

    def clear_queue(self):
        self.queue.clear()
        self.queue_modified.emit()

    def clear_history(self):
        self.history.clear()
        self.history_modified.emit()

        
    
    def next_song(self):
        '''
        Parameters below describe behaviour based on play loop mode. Returns the new current playing song.
        

        :param single: Do not advance queue. Return currently playing song. Does not add song to history.

        :param playlist: Advance queue to the next available song. Add skipped song to the end of the queue. Return currently playing song. If no song in queue, repeat current song. 
        Adds previously played song to history.

        :param none: Advance queue to the next available song. Remove skipped song from the queue. Return currently playing song. Adds previously
        '''
        if not self._can_advance():
            logging.warning("Cannot play next song!")
            return None
        elif self.loop_mode == LoopMode.SINGLE:
            return self.playing
        self._advance_playback()
        return self.playing
        
    def previous_song(self):
        '''
        If history exists, revert current playing song to that song. Return that song. 
        '''

        if self.playing and self.history:
            self._queue_song_front(self.playing)
            song = self._pop_history()
            if song:
                self._set_playing(song)
            title,artist = self.playing.get_info("title"), self.playing.get_info("artist")
            logging.info(f"Returned to previous track. Now playing {title} by {artist}")
        elif not self.playing:
            logging.warning("Not currently playing a song!")
        elif not self.history:
            logging.warning("No music history!")
        return self.playing

    def print_queue(self):
        '''
        Debug function. Prints a representation of the current songs in the queue.
        
        '''
        if self.playing:
            title = self.playing.get_info("title")
            logging.info(f"Currently playing {title}")
        else:
            logging.info("Nothing currently playing")
        if self.queue:
            logging.info("Current queue:")
            for i, song in enumerate(self.queue, start=1):
                title = song.get_info("title")
                logging.info(f"{i}. {title}")
    
    def return_queue(self):
        return self.queue
    
    def shuffle_queue(self):
        '''
        Permanent action. Shuffles the currently existing queue.
        
        :param self: Description
        '''
        tmp = list(self.queue)
        shuffle(tmp)
        self.queue = deque(tmp)
        self.queue_modified.emit()
    
    
    def remove_song(self, song : Song):
        if song in self.queue:
            self.queue.remove(song)
            logging.info(f"{song.get_info("title")} was removed from the queue\n")
        else:
            logging.warning(f"{song.get_info("title")} is not in queue!\n")
    
    def pop_song(self, index : int):
        if (0 <= index < len(self.queue)):
            tmp = list(self.queue)
            tmp.pop(index)
            self.queue = deque(tmp)
        else:
            logging.warning("Indexes cannot be out of queue range!")

    def swap_songs(self, index1: int, index2: int):
        if (0 <=max(index1, index2) < len(self.queue)):
            song1, song2 = self.queue[index1], self.queue[index2]
            self.queue[index1], self.queue[index2] = song2, song1
        else:
            logging.warning("Indexes cannot be out of queue range!")
