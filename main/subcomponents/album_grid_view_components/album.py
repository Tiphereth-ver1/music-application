from ...song import Song
from typing import List, Optional

class Album:

    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
        self.songs: list[Song] = []

    def _parse_track(self, trck):
        if not trck:
            return 0
        if isinstance(trck, list):
            trck = trck[0]
        return int(str(trck).split("/")[0])   
    
    def get_name(self):
        return self.name


    def _index_songs(self):
        self.songs.sort(key=lambda s: (int(s.get_info("track") or 999), str(s.get_info("title") or "ZZZ")))


    def add_song(self, song: Song):
        self.songs.append(song)
        self._index_songs()
    
            
    def add_songs(self, songs: list[Song]):
        '''
        Adds multiple songs from a list of songs
        
        :param self: Description
        :param songs: Description
        :type songs: List(Song)
        '''
        for song in songs:
            self.add_song(song)
                
    def remove_song(self, song: Song):
        if song in self.songs:
            self.songs.remove(song)

    def get_cover(self) -> Optional[bytes]:
        if self.songs:
            for song in self.songs:
                art = song.get_art()
                if art:
                    return art
        return None
    
    def print_songs(self):
        for i in range(0,len(self.songs)):
            print(f"{i+1}: {self.songs[i].get_info("title")}")
    
    def get_songs(self) -> list[Song]:
        return self.songs
    
    def get_song(self, idx :int) -> Song:
        return self.songs[idx]

    def info_check(self) -> tuple[str, str]:
        return (self.name, self.artist)
    
# songs = [
#     Song("music/beat_it.mp3"),
#     Song("music/thriller.mp3"),
#     Song("music/billie_jean.mp3"),
#     Song("music/this_girl_is_mine.mp3"),
# ]

# album = Album("Thriller", "Michael Jackson")
# album.add_songs(songs)
# album.print_songs()

