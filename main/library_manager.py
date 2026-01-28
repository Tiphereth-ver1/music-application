from pathlib import Path
import sqlite3
from typing import Iterator
from .song_subclasses import MP3Song, M4ASong, FLACSong
from . import Song
from PySide6.QtCore import QObject, Signal


#SQLite basics! Creating a conn tool to have an accessible database.
# conn = sqlite3.connect("music.db")

#Cursor tool is connected to conn to execute commands
# cursor = conn.cursor()

#Executing cursoe commands take place inside """ and are saved with commit()
#INTEGER PRIMARY KEY is an automatically assigned "id" that allows for indexing of songs and other things
#UNIQUE is a tag that adds a check to make sure all elements of that are unique
# cursor.execute("""
# DROP TABLE songs
# """)
# conn.commit()


# cursor.execute("""
# CREATE TABLE IF NOT EXISTS songs (
#     id INTEGER PRIMARY KEY,
#     title TEXT,
#     artist TEXT,
#     album TEXT,
#     file_path TEXT UNIQUE NOT NULL,
#     duration REAL,
#     file_extension TEXT,
#     mtime INTEGER
# )
# """)
# conn.commit()


# conn.commit()

# The ideal way to insert values into a db, to prevent SQL injection
# cursor.execute("""
# INSERT INTO songs (title, artist, album, file_path, duration)
# VALUES (?, ?, ?, ?, ?)
# """, (title, artist, album, path, duration))

# conn.commit()

"""
SELECT * FROM songs; -> General selection a group
SELECT title, artist FROM songs WHERE album = 'Album Y'; -> FROM provides location of target group and WHERE provides conditions for actual selection
DELETE FROM songs WHERE id = 3; -> Deletion with WHERE and FROM
DROP TABLE songs -> used to remove an existing table
UPDATE songs
SET title = 'New Title'
WHERE id = 3;
"""

# Upserting example, a method that allows handling of duplicates more effectively

# cursor.execute("""
#     INSERT INTO songs (title, artist, album, file_path, duration, file_extension)
#     VALUES (?, ?, ?, ?, ?, ?)
#     ON CONFLICT(file_path) DO UPDATE SET
#         title=excluded.title,
#         artist=excluded.artist,
#         album=excluded.album,
#         duration=excluded.duration,
#         file_extension=excluded.file_extension
# """, (...))

RETURN_VALUES = ["id","title","artist","album","file_path","duration","file_extension","mtime"]

class LibraryService(QObject):

    def __init__(self):
        super().__init__()
        self._song_cache: dict[int, Song] = {}
        # self.conn = sqlite3.connect("music.db")
        # self.cursor = self.conn.cursor()
        pass

    def _base_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def _to_rel(self, abs_path: Path) -> Path:
        return abs_path.relative_to(self._base_dir())

    def _to_abs(self, rel_path: Path) -> Path:
        return self._base_dir() / rel_path


    def _initialise_database(self, conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                album_artist TEXT NOT NULL,
                year INTEGER,
                cover_path TEXT,
                UNIQUE(title, album_artist)
            );

            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                title TEXT,
                artist TEXT,
                album TEXT,
                album_artist TEXT,
                album_id INTEGER,
                file_path TEXT UNIQUE NOT NULL,
                duration REAL,
                file_extension TEXT,
                mtime INTEGER NOT NULL,
                size INTEGER NOT NULL,
                FOREIGN KEY(album_id) REFERENCES albums(id)
            );
            """)
        conn.commit()

    def _initialise_song(self, file_path: Path) -> tuple[Song, str] | None:
        suf = file_path.suffix.lower()
        if suf == ".mp3":
            return (MP3Song(file_path), "MP3")
        if suf == ".m4a":
            return (M4ASong(file_path), "M4A")
        if suf == ".flac":
            return (FLACSong(file_path), "FLAC")
        return None

    def enumerate_audio_files(self) -> list[Path]:
        base_dir = Path(__file__).resolve().parent.parent
        music_folder = base_dir / "music"
        files : list[Path] = []
        for pattern in ("*.mp3", "*.m4a", "*.flac"):
            files.extend(music_folder.rglob(pattern))
        return files
    
    def upsert_album(self, cursor, album_name, album_artist):
        pass

    def upsert_song_from_path(self, conn, cursor, song: Song, abs_path: Path) -> None:
        rel_path = self._to_rel(abs_path)
        rel_str = str(rel_path)

        st = abs_path.stat()
        mtime = int(st.st_mtime)
        size = int(st.st_size)


        cursor.execute("SELECT id, mtime, size FROM songs WHERE file_path = ?", (rel_str,))
        row = cursor.fetchone()

        if row is None:
            # new file -> parse tags
            song, ext = self._initialise_song(abs_path)
            album_id = self.upsert_album(cursor, song.get_info("album"), song.get_info("album_artist"))
            cursor.execute("""
                INSERT INTO songs (title, artist, album_id, file_path, duration, file_extension, mtime, size)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (...))
            return "added"

        song_id, old_mtime, old_size = row
        if old_mtime == mtime and old_size == size:
            return "unchanged"

        # changed -> re-parse tags and update
        song, ext = self._initialise_song(abs_path)
        album_id = self.upsert_album(cursor, song.get_info("album"), song.get_info("album_artist"))

        cursor.execute("""
            UPDATE songs
            SET title=?, artist=?, album_id=?, duration=?, file_extension=?, mtime=?, size=?
            WHERE id=?
        """, (song.get_info("title"),
        song.get_info("artist"),
        song.get_info("album"),
        song.get_info("album_artist"),
        album_id,
        song.get_song_length(),
        ext,
        mtime,
        size,
        song_id
    ))

        self.invalidate_song(song_id)
        return "updated"



    def filepath_to_songs(self, conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        music_folder = base_dir / "music"

        def insert_or_update(song: Song, rel_path: Path, ext_label: str, mtime: int) -> None:
            cursor.execute("""
                INSERT INTO songs (title, artist, album, album_artist, file_path, duration, file_extension, mtime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(file_path) DO UPDATE SET
                    title = excluded.title,
                    artist = excluded.artist,
                    album = excluded.album,
                    duration = excluded.duration,
                    file_extension = excluded.file_extension,
                    mtime = excluded.mtime
            """, (
                song.get_info("title"),
                song.get_info("artist"),
                song.get_info("album"),
                song.get_info("album_artist"),
                str(rel_path),
                song.get_song_length(),
                ext_label,
                mtime
            ))

        for file_path in self.enumerate_audio_files():
            init = self._initialise_song(file_path)
            if init is None:
                continue
            song, ext = init
            rel_path = file_path.relative_to(base_dir)
            mtime = int(file_path.stat().st_mtime)
            insert_or_update(song, rel_path, ext, mtime)

        conn.commit()

    def SongFactory(self, cursor: sqlite3.Cursor, song_id: int) -> Song:
        if song_id in self._song_cache:
            return self._song_cache[song_id]

        cursor.execute("SELECT file_path FROM songs WHERE id = ?", (song_id,))
        row = cursor.fetchone()
        if row is None:
            raise KeyError(f"No song with id={song_id}")

        rel_path = Path(row[0])
        abs_path = self._to_abs(rel_path)


        init = self._initialise_song(abs_path)
        if init is None:
            raise ValueError(f"Unsupported file type: {abs_path}")

        song, _ = init
        self._song_cache[song_id] = song
        return song
    
    def invalidate_song(self, song_id: int):
        self._song_cache.pop(song_id, None)



library_service = LibraryService()
conn = sqlite3.connect("music.db")
cursor = conn.cursor()
library_service.filepath_to_songs(conn, cursor)
song = library_service.SongFactory(cursor, 1)
print(song.get_info("title"))
song = library_service.SongFactory(cursor, 21)
print(song.get_info("title"))
