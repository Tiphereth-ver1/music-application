from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TYER, TDRC, TCON, COMM, APIC
from playlist import Playlist
from song import Song
from collections import deque
from random import shuffle
import logging
logging.basicConfig(level=logging.DEBUG)


LOOP_MODES = ["single", "playlist", "none"]

class Player:

    def __init__(self):
        self.playing = None
        self.queue : deque[Song] = deque()
        self.loop_mode = "none" # single, playlist, none
        self.history : list[Song] = []
        self.shuffle = False

    def _push_history(self, song: Song):
        if song:
            self.history.append(song)
    
    def _return_last_played(self):
        return self.history.pop(-1)

    def _set_playing(self, song: Song):
        self.playing = song

    def _advance_queue(self):
        if not self.queue:
            return None
        return self.queue.popleft()

    def _queue_songs(self, songs : list[Song]):
        self.queue.extend(songs)

    def _queue_song_back(self, song : Song):
        self.queue.extend(song)


    def _queue_song_front(self, song : Song):
        self.queue.appendleft(song)


    def toggle_loop(self, mode: str):
        if mode in LOOP_MODES:
            self.loop_mode = mode
            logging.info(f"Set loop mode to {mode}")
        else:
            logging.warning("Invalid loop mode")

    
    
    def next_song(self):
        '''
        Advances queue to the next available song depending on loop mode. Returns the new current playing song. Adds currently playing song to history provided it is not in single loop mode.
        single: Do not advance queue. Return currently playing song.
        playlist: Advance queue to the next available song. Add skipped song to the end of the queue. Return currently playing song.
        none: Advance queue to the next available song. Remive skipped song from the queue. Return currently playing song.
        '''
        if not self.playing or not self.queue:
            logging.warning("Cannot play next song!")
            return None
                
        if self.loop_mode == "single":
            return self.playing

        self._push_history(self.playing)

        if self.loop_mode == "playlist":
            self._queue_song_back(self.playing)

        self.playing = self._advance_queue()
        title, artist = self.playing.get_info("title"), self.playing.get_info("artist")
        logging.info(f"Playing {title} by {artist}")
        return self.playing
        
    def previous_song(self):
        '''
        If history exists, revert current playing song to that song. Return that song. 
        '''

        if self.playing and self.history:
            self._queue_song_front(self.playing)
            self.playing = self._return_last_played()
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
    
    def shuffle_queue(self):
        if not self.shuffle:
            tmp = list(self.queue)
            shuffle(tmp)
            self.queue = deque(tmp)
            logging.info("Shuffle turned on")
        else:
            logging.info("Shuffle turned off")
        self.shuffle = not self.shuffle
    
    def remove_song(self,song : Song):
        if song in self.queue:
            self.queue.remove(song)
            logging.info(f"{song.get_info("title")} was removed from the queue\n")
        else:
            logging.warning(f"{song.get_info("title")} is not in queue!\n")

    def insert_song(self,song : Song, pos : int):
        tmp = list(self.queue)
        tmp.insert(pos, song)
        self.queue = deque(tmp)

    def skip(self, n: int):
        '''
        Skip up to n elements currently located at the front of the queue.
        
        :param self: Description
        :param n: Description
        :type n: int
        '''
        if len(self.queue) < n:
            logging.warning("Cannot skip more elements than in the queue")
            return
        for i in range(n):
            self.next_song()
        logging.info(f"{n} songs skipped\n")


playlist = Playlist()
song = Song("beat_it.mp3")
song2 = Song("thriller.mp3")
song3 = Song("billie_jean.mp3")
song4 = Song("this_girl_is_mine.mp3")
playlist.add_song(song)
playlist.add_song(song2)
playlist.add_song(song3)
playlist.add_song(song4)

player = Player()
player.queue_songs(playlist.get_songs())
player.toggle_loop("single")
player.next_song()
player.print_queue()
player.toggle_loop("playlist")
player.next_song()
player.print_queue()
player.next_song()
player.shuffle_queue()
player.print_queue()
player.previous_song()
player.print_queue()
player.previous_song()
player.print_queue()
player.previous_song()
player.print_queue()
player.previous_song()
player.previous_song()
player.previous_song()
player.previous_song()
player.previous_song()
player.previous_song()
player.previous_song()
player.print_queue()

