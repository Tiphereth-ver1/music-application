from collections import deque
from random import shuffle
import logging
logging.basicConfig(level=logging.DEBUG)
from PySide6.QtCore import QObject, Signal
from .library_manager import LibraryService

from enum import Enum, auto

class LoopMode(Enum):
    NONE = "none"
    PLAYLIST = "playlist"
    SINGLE = "single"

class Player(QObject):
    queue_modified = Signal()
    history_modified = Signal()
    history_appended = Signal(int)
    history_removed = Signal(int)
    queue_appended = Signal(int)
    queue_popped = Signal(int)
    queue_prepended = Signal(int)
    '''
    To use a signal, define it outside of the initialisation. When in code, use self.function.emit()
    '''

    def __init__(self, library : LibraryService):
        super().__init__()
        self.lib = library
        self.playing = None
        self.queue : list[int] = []
        self.loop_mode : LoopMode = LoopMode.NONE
        self.history : list[int] = []
        self.shuffle = False

    def _stop_playing(self):
        self.playing = None

    def _log_playing(self, song_id: int):
        meta = self.lib.get_song_meta(song_id)
        logging.info(f"Playing {meta.title} by {meta.artist}")
    
    def _begin_playback(self):
        if not self.playing and self.queue:
            self._set_playing(self._advance_queue())

    def _push_history(self, song_id: int) -> None:
        if song_id is not None:
            self.history.append(song_id)
            self.history_appended.emit(song_id)
    
    def _pop_history(self) -> int | None:
        if self.history:
            history = self.history.pop()
            self.history_removed.emit(history)
        else: 
            history = None
        return history
    
    def _set_playing(self, song_id: int) -> None:
        self.playing = song_id
        if song_id is not None:
            self._log_playing(song_id)
    
    def _can_advance(self) -> bool:
        '''
        Returns if 
        
        :param self: Description
        :return: Description
        :rtype: bool
        '''
        if self.loop_mode == LoopMode.SINGLE:
            return True
        if self.queue:
            return True
        if self.loop_mode == LoopMode.PLAYLIST:
            return True
        return False
    

    def _advance_queue(self) -> int | None:
        song_id = self.queue.pop(0)
        if not song_id:
            return None
        
        self.queue_popped.emit(song_id)
        return song_id
        
    def _advance_playback(self) -> None:
        self._push_history(self.playing)

        if self.loop_mode == LoopMode.PLAYLIST:
            self._queue_song_back(self.playing)

        self._set_playing(self._advance_queue())

    def _queue_songs(self, songs : list[int]) -> None:
        for song_id in songs:
            self._queue_song_back(song_id)
        # self.queue_modified.emit()
    
    def _queue_songs_front(self, songs : list[int]) -> None:
        for song_id in reversed(songs):
            self._queue_song_front(song_id)
        # self.queue_modified.emit()

    def _queue_song_back(self, song_id : int) -> None:
        self.queue.append(song_id)
        self.queue_appended.emit(song_id)

    def _queue_song_front(self, song_id : int) -> None:
        self.queue.insert(0,song_id)
        self.queue_prepended.emit(song_id)
    
    def _queue_song_index(self, index : int, song_id : int) -> None:
        self.queue.insert(index, song_id)
        self.queue_modified.emit()

    def get_playing(self) -> int:
        return self.playing

    def toggle_loop(self, mode: LoopMode) -> None:
        self.loop_mode = mode
        logging.info(f"Set loop mode to {mode}")

    def play_now(self,song_id):
        self.clear_queue()
        self._push_history(self.playing)
        self._set_playing(song_id)

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
            song_id = self._pop_history()
            if song_id is not None:
                self._set_playing(song_id)
            meta = self.lib.get_song_meta(self.playing)
            logging.info(f"Returned to previous track. Now playing {meta.title} by {meta.artist}")
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
            meta = self.lib.get_song_meta(self.playing)
            logging.info(f"Currently playing {meta.title}")
        else:
            logging.info("Nothing currently playing")
        if self.queue:
            logging.info("Current queue:")
            for i, song_id in enumerate(self.queue, start=1):
                meta = self.lib.get_song_meta(song_id)
                title = meta.title
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
    
    
    def remove_song(self, song_id : int):
        meta = self.lib.get_song_meta(song_id)
        if song_id in self.queue:
            self.queue.remove(song_id)
            logging.info(f"{meta.title} was removed from the queue\n")
        else:
            logging.warning(f"{meta.title} is not in queue!\n")
    
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
