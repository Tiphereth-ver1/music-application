from pathlib import Path
import sqlite3
from typing import Iterator
from .song_subclasses import MP3Song, M4ASong, FLACSong
from .song import Song
from PySide6.QtCore import QObject, Signal
from enum import Enum
from .art_cache import ArtCache
import hashlib, time, logging

def get_image_cache(self, hex: str, size : int, ext : str = ".jpg"):
    path = self.cache_dir / hex[:2] / hex / f"{size}{ext}"
    if path.exists():
        return path
    return None



def cache_image_bytes(data: bytes | None, cache_dir: Path, ext=".jpg") -> Path | None:
    if not data:
        return None
    digest = hashlib.sha256(data).hexdigest()
    path = cache_dir / f"{digest}{ext}"

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

    return path

class RETURN_VALUES(Enum):
    ID = "id"
    TITLE = "title"
    ALBUM = "album"
    ARTIST = "artist"
    ALBUM_ARTIST = "album_artist"
    DURATION = "duration"
    YEAR = "year"
    FILE_PATH = "file_path"
    FILE_EXTENSION = "file_extension"
    MTIME = "mtime"
    SIZE = "size"

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass(frozen=True, slots=True)
class SongMeta:
    """
    SongMeta class. Designed to be more lightweight in RAM usage than the song class with no direct access to file art.
    """
    id: int
    title: str | None
    artist: str | None
    album: str | None
    album_artist: str | None
    duration: float
    track: int | None
    track_total: int | None
    year: int | None
    file_path: Path          # relative path from DB
    art_hex: str
    cover_path: Optional[Path]  # relative, from albums table

@dataclass(frozen=True, slots=True)
class AlbumMeta:
    id: int
    title: str
    album_artist: str
    year: int | None
    cover_path: Optional[Path]   # relative
    art_hex: str

@dataclass(frozen=True, slots=True)
class PlaylistMeta:
    id: int
    title: str
    cover_path: Optional[Path]   # relative
    art_hex: str


class LibraryService(QObject):
    library_changed = Signal()
    playlists_changed = Signal()

    def __init__(self, db_path: Path):
        super().__init__()
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.cursor = self.conn.cursor()
        self._song_cache: dict[int, Song] = {}
        self._meta_cache: dict[int, SongMeta] = {}
        self._album_cache: dict = {}
        self.art_dir = self._base_dir() / "cache" / "album_art"
        self.art_cache = ArtCache(self.art_dir)
        
        pre_startup = round(time.time()*1000)
        # self._clear_database()
        self._initialise_database()
        self.scan_library()
        startup = round(time.time()*1000)
        logging.info(f"DB initialisation time : {startup - pre_startup}")

    @staticmethod
    def _fold(s: str | None) -> str | None:
        return s.casefold() if s else None

    def _base_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def _to_rel(self, abs_path: Path) -> Path:
        return abs_path.relative_to(self._base_dir())

    def _to_abs(self, rel_path: Path) -> Path:
        return self._base_dir() / rel_path

    def _clear_database(self) -> None:
        with self.conn:
            self.conn.execute("PRAGMA foreign_keys = OFF;")

            for (name,) in self.conn.execute("""
                SELECT name FROM sqlite_master WHERE type='trigger';
            """).fetchall():
                self.conn.execute(f'DROP TRIGGER IF EXISTS "{name}";')

            for (name,) in self.conn.execute("""
                SELECT name FROM sqlite_master WHERE type='view';
            """).fetchall():
                self.conn.execute(f'DROP VIEW IF EXISTS "{name}";')

            for table in ("playlist_songs", "playlists", "songs", "albums"):
                self.conn.execute(f'DROP TABLE IF EXISTS "{table}";')

            self.conn.execute("PRAGMA foreign_keys = ON;")

    def _initialise_database(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                album_artist TEXT NOT NULL,
                year INTEGER,
                cover_path TEXT,
                art_hex TEXT,
                UNIQUE(title, album_artist)
            );""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            artist TEXT,
            album TEXT,
            album_artist TEXT,
            album_id INTEGER,
            file_path TEXT UNIQUE NOT NULL,
            art_hex TEXT,
            duration REAL,
            year INTEGER,
            track INTEGER,
            track_total INTEGER,
            file_extension TEXT,
            mtime INTEGER NOT NULL,
            size INTEGER NOT NULL,

            title_fold TEXT,
            artist_fold TEXT,
            album_fold TEXT,

            FOREIGN KEY(album_id) REFERENCES albums(id)
                );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                created_at INTEGER,
                updated_at INTEGER,
                cover_path TEXT,
                art_hex TEXT,
                UNIQUE(title));
                """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlist_songs (
                playlist_id INTEGER NOT NULL,
                song_id INTEGER NOT NULL,
                position INTEGER,
                PRIMARY KEY (playlist_id, song_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE);
                """)
        
        self.conn.commit()

    def _initialise_song(self, file_path: Path) -> tuple[Song, str] | None:
        suf = file_path.suffix.lower()
        if suf == ".mp3":
            return (MP3Song(file_path), "MP3")
        if suf == ".m4a":
            return (M4ASong(file_path), "M4A")
        if suf == ".flac":
            return (FLACSong(file_path), "FLAC")
        return None
    
    def get_song_info(self, song_id : int, return_value: RETURN_VALUES) -> str:
        column = return_value.value
        self.cursor.execute(
            f"SELECT {column} FROM songs WHERE id = ?",
            (song_id,)
        )
        row = self.cursor.fetchone()[0]
        return str(row)
    
    def get_song_meta(self, song_id: int) -> SongMeta:
        cached = self._meta_cache.get(song_id)
        if cached is not None:
            return cached

        self.cursor.execute("""
            SELECT
                s.id, s.title, s.artist, s.album, s.album_artist,
                s.duration, s.year, s.track, s.track_total, 
                s.file_path, s.art_hex, a.cover_path
            FROM songs s
            LEFT JOIN albums a ON a.id = s.album_id
            WHERE s.id = ?
        """, (song_id,))
        row = self.cursor.fetchone()
        if row is None:
            raise KeyError(f"No song with id={song_id}")

        (sid, title, artist, album, album_artist,
            duration, year, track, track_total, file_path, art_hex, cover_path) = row

        song_meta = SongMeta(
            id=sid,
            title=title,
            artist=artist,
            album=album,
            album_artist=album_artist,
            duration=float(duration or 0.0),
            year=year,
            track=track,
            track_total=track_total,
            file_path=Path(file_path),
            art_hex = art_hex,
            cover_path=Path(cover_path) if cover_path else None
        )

        self._meta_cache[song_id] = song_meta
        return song_meta

    def _upsert_album(self, title: str, album_artist: str, year: int | None, cover_path: str | None, art_hex: str | None) -> int:
        self.cursor.execute(
            """
            INSERT INTO albums (title, album_artist, year, cover_path, art_hex)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(title, album_artist) DO UPDATE SET
                year = COALESCE(excluded.year, albums.year),
                cover_path = COALESCE(excluded.cover_path, albums.cover_path),
                art_hex = COALESCE(excluded.art_hex, albums.art_hex)

        """, (title, album_artist, year, str(cover_path), art_hex))

        self.cursor.execute("""
        SELECT id FROM albums
        WHERE title = ? AND album_artist = ?
        """, (title, album_artist))
        row = self.cursor.fetchone()[0]
        return row

    def _remove_deleted_songs(self, seen: set[str]) -> int:
        # all song paths currently in DB
        self.cursor.execute("SELECT id, file_path FROM songs")
        rows = self.cursor.fetchall()

        missing_ids: list[int] = [sid for (sid, fp) in rows if fp not in seen]
        if not missing_ids:
            return 0

        for sid in missing_ids:
            self.invalidate_song(sid)

        CHUNK = 500
        for i in range(0, len(missing_ids), CHUNK):
            chunk = missing_ids[i:i+CHUNK]
            q = ",".join(["?"] * len(chunk))
            self.cursor.execute(f"DELETE FROM songs WHERE id IN ({q})", chunk)

        return len(missing_ids)

    def scan_library(self) -> dict:
        seen : set = set()
        counts = {"added": 0, "updated": 0, "unchanged": 0, "deleted" : 0}
        with self.conn:  # commits if success, rollbacks on exception
            for abs_path in self.enumerate_audio_files():
                rel_str = str(self._to_rel(abs_path))
                seen.add(rel_str)
                r, _ = self.upsert_song_from_path(abs_path)
                counts[r] += 1
            counts["deleted"] += self._remove_deleted_songs(seen)
            logging.info(counts)
            self._album_removal()
        self.library_changed.emit()
        return counts
    
    def _album_removal(self) -> None:
        self.cursor.execute("""
                    DELETE FROM albums
            WHERE id NOT IN (
            SELECT DISTINCT album_id FROM songs WHERE album_id IS NOT NULL
            );
            """)

    def post_album_edit_check(self) -> None:
        with self.conn:  # commits if success, rollbacks on exception
            self._album_removal()
        self.library_changed.emit()
    
    def post_album_add_check(self) -> None:
        self.library_changed.emit()

    def post_playlist_edit_check(self) -> None:
        self.playlists_changed.emit()


    def upsert_song_from_path(self, abs_path: Path) -> tuple[str, Song | None]:
        rel_path = self._to_rel(abs_path)
        rel_str = str(rel_path)

        st = abs_path.stat()
        mtime = int(st.st_mtime)
        size = int(st.st_size)

        self.cursor.execute("SELECT id, mtime, size FROM songs WHERE file_path = ?", (rel_str,))
        row = self.cursor.fetchone()
    
        if row is None:
            # new file -> parse tags
            init = self._initialise_song(abs_path)
            if init is None:
                return "unchanged"
            song, ext = init

            art_bytes = song.get_art()
            art_hex = self.art_cache.get_hex_cache(art_bytes)
            self.art_cache.cache_image_bytes(art_bytes, ext=".jpg")
            #check to have either album artist or artist as an album
            album, album_artist = self._album_info_check(song)

            title = song.get_info("title")
            artist = song.get_info("artist")

            if art_hex:
                self.art_cache.cache_image_bytes(art_bytes, ext=".jpg")
                art_path_256 = self.art_cache.get_image_cache(art_hex, 256)
            else:
                art_path_256 = None

            album_id = self._upsert_album(album, album_artist, song.get_info("year"), str(art_path_256), art_hex)
            self.cursor.execute("""
                INSERT INTO songs (
                    title, artist, album, album_artist, album_id,
                    file_path, art_hex, duration, year, track, track_total,
                    file_extension, mtime, size,
                    title_fold, artist_fold, album_fold
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title,
                artist,
                album,
                album_artist,
                album_id,
                rel_str,
                art_hex,
                song.get_song_length(),
                song.get_info("year"),
                song.get_info("track"),
                song.get_info("track_total"),
                ext,
                mtime,
                size,
                self._fold(title),
                self._fold(artist),
                self._fold(album),
            ))


            self.conn.commit()
            return "added", song

        song_id, old_mtime, old_size = row
        if old_mtime == mtime and old_size == size:
            return "unchanged", None

        # changed -> re-parse tags and update
        init = self._initialise_song(abs_path)
        if init is None:
            return "unchanged", None  # or raise
        song, ext = init

        art_bytes = song.get_art()
        art_hex = self.art_cache.get_hex_cache(art_bytes)
        self.art_cache.cache_image_bytes(art_bytes, ext=".jpg")
        #check to have either album artist or artist as an album
        album, album_artist = self._album_info_check(song)

        title = song.get_info("title")
        artist = song.get_info("artist")

        if art_hex:
            self.art_cache.cache_image_bytes(art_bytes, ext=".jpg")
            art_path_256 = self.art_cache.get_image_cache(art_hex, 256)
        else:
            art_path_256 = None

        #check to have either album artist or artist as an album
        album, album_artist = self._album_info_check(song)
        album_id = self._upsert_album(album, album_artist, song.get_info("year"), art_path_256, art_hex)

        self.cursor.execute("""
            UPDATE songs
            SET
                title=?,
                artist=?,
                album=?,
                album_artist=?,
                album_id=?,
                file_path=?,
                art_hex=?,
                duration=?,
                year=?,
                track=?,
                track_total=?,
                file_extension=?,
                mtime=?,
                size=?,
                title_fold=?,
                artist_fold=?,
                album_fold=?
            WHERE id=?
        """, (
            title,
            artist,
            album,              
            album_artist,
            album_id,
            rel_str,
            art_hex,
            song.get_song_length(),
            song.get_info("year"),
            song.get_info("track"),
            song.get_info("track_total"),
            ext,
            mtime,
            size,
            self._fold(title),
            self._fold(artist),
            self._fold(album),
            song_id
        ))

        self.conn.commit()

        self.invalidate_song(song_id)
        return "updated", song

    def SongFactory(self, song_id: int) -> Song:
        if song_id in self._song_cache:
            return self._song_cache[song_id]

        self.cursor.execute("SELECT file_path FROM songs WHERE id = ?", (song_id,))
        row = self.cursor.fetchone()
        if row is None:
            raise KeyError(f"No song with id={song_id}")

        rel_path = Path(row[0])
        abs_path = self._to_abs(rel_path)


        init = self._initialise_song(abs_path)
        if init is None:
            return "unchanged"
        song, ext = init

        self._song_cache[song_id] = song
        return song
    
    def songs_from_ids(self, ids: list[int]) -> list[Song]:
        return [self.SongFactory(i) for i in ids]
    
    def get_matching_songs(self, text : str) -> list[int]:
        self.cursor.execute("""
        SELECT id, title, album_artist, album, artist
        FROM songs
        WHERE title_fold  LIKE lower(?) || '%'
        OR artist_fold LIKE lower(?) || '%'
        OR album_fold  LIKE lower(?) || '%'
        LIMIT 200;
        """, (text,text, text,))
        return [r[0] for r in self.cursor.fetchall()]


    def _album_info_check(self, song : Song) -> tuple[str,str]:
        album = song.get_info("album")
        if not album:
            album = "Unknown Album"

        album_artist = song.get_info("album_artist")
        if not album_artist:
            album_artist = song.get_info("artist")
        if not album_artist:
            album_artist = "Unknown Artist"
        
        return album, album_artist
    
    def enumerate_audio_files(self) -> list[Path]:
        base_dir = Path(__file__).resolve().parent.parent
        music_folder = base_dir / "music"
        files : list[Path] = []
        for pattern in ("*.mp3", "*.m4a", "*.flac"):
            files.extend(music_folder.rglob(pattern))
        return files

    def abs_song_path(self, song_id: int) -> Path:
        meta = self.get_song_meta(song_id)
        return self._to_abs(meta.file_path)

    def abs_cover_path(self, song_id: int) -> Path | None:
        meta = self.get_song_meta(song_id)
        if meta.cover_path is None:
            return None
        return self._to_abs(meta.cover_path)

    def invalidate_song(self, song_id: int) -> None:
        self._song_cache.pop(song_id, None)
        self._meta_cache.pop(song_id, None)
    
    def invalidate_album_cache(self, album_id : int) -> None:
        if album_id in self._album_cache.keys():
            self._album_cache.pop(album_id)
    
    def get_album_from_id(self, album_id : int) -> AlbumMeta:
        cached = self._album_cache.get(album_id)
        if cached is not None:
            return cached
        else: 
            self.cursor.execute("""
                SELECT id, title, album_artist, year, cover_path, art_hex
                FROM albums
                WHERE id = ?
            """, (album_id,))

            row = self.cursor.fetchone()

            if row is None:
                return None

            aid, title, album_artist, year, cover, hex = row

            meta = AlbumMeta(
                id=aid,
                title=title,
                album_artist=album_artist,
                year=year,
                cover_path=Path(cover) if cover else None,
                art_hex = hex
            )

            self._album_cache[album_id] = meta
            return meta

    def get_albums(self, order : RETURN_VALUES) -> list[AlbumMeta]:
        albums = []
        self.cursor.execute(f"""
            SELECT id FROM albums
            ORDER BY {order.value} COLLATE NOCASE, title COLLATE NOCASE
        """)
        rows = self.cursor.fetchall()
        return [
            self.get_album_from_id(album_id=aid)
            for (aid,) in rows
            ]

    def get_album_song_ids(self, album_id: int) -> list[int]:
        self.cursor.execute("""
            SELECT id
            FROM songs
            WHERE album_id = ?
            ORDER BY COALESCE(track, 999), title COLLATE NOCASE
        """, (album_id,))
        return [r[0] for r in self.cursor.fetchall()]

    def abs_album_cover_path(self, album_id: int, size : int) -> Path | None:
        self.cursor.execute("SELECT art_hex FROM albums WHERE id = ?", (album_id,))
        row = self.cursor.fetchone()
        if not row or not row[0]:
            return None
        return self.art_cache.get_image_cache(row, size)
    
    def get_songs_from_playlist(self, playlist_id : int) -> list[int]:
        self.cursor.execute("""
            SELECT song_id 
            FROM playlist_songs
            WHERE playlist_id = ?
            ORDER BY COALESCE(position, 999)
            """,(playlist_id,))
        return [r[0] for r in self.cursor.fetchall()]
    
    def upsert_playlist(self, title : str):
        self.cursor.execute("""
        INSERT INTO playlists (title, created_at, updated_at)
        VALUES (?,?,?)
        ON CONFLICT(title) DO UPDATE SET
                cover_path = COALESCE(excluded.cover_path, playlists.cover_path)
        """, (title, 0, 0))
        self.conn.commit()

    def modify_playlist(self, playlist_id : int, title : str, cover_path : str):
        self.cursor.execute("""
            UPDATE playlists
            SET title = ?, cover_path = ?
            WHERE id = ?;
        """, (title, cover_path, playlist_id))

        if self.cursor.rowcount == 0:
            raise KeyError(f"Playlist {playlist_id} does not exist")

        self.conn.commit()

    def get_playlist_meta_by_id(self, playlist_id : int) -> PlaylistMeta:
        self.cursor.execute("""
            SELECT id, title, cover_path
            FROM playlists
            WHERE id = ?
            ORDER BY title COLLATE NOCASE
        """, (playlist_id,))

        (pid, title, cover) = self.cursor.fetchone()
        return PlaylistMeta(
                id= pid,
                title=title,
                cover_path=Path(cover) if cover else None
            )

    def get_playlists(self) -> list[PlaylistMeta]:
        self.cursor.execute("""
            SELECT id, title, cover_path
            FROM playlists
            ORDER BY title COLLATE NOCASE
        """)
        rows = self.cursor.fetchall()
        return [
            PlaylistMeta(
                id=pid,
                title=title,
                cover_path=Path(cover) if cover else None
            )
            for (pid, title, cover) in rows
        ]

    def delete_playlist(self, playlist_id : int) -> None :
        self.cursor.execute("""
            DELETE FROM playlists
            WHERE id = ?

        """, (playlist_id,))

    def _exists(self, table: str, id_: int) -> bool:
        self.cursor.execute(f"SELECT 1 FROM {table} WHERE id = ? LIMIT 1;", (id_,))
        return self.cursor.fetchone() is not None

    def insert_into_playlist(self, *, song_id: int, playlist_id: int) -> None:
        self.cursor.execute(
            """
            SELECT COALESCE(MAX(position), 0) + 1
            FROM playlist_songs
            WHERE playlist_id = ?
            """,
            (playlist_id,)
        )
        (next_pos,) = self.cursor.fetchone()

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO playlist_songs (playlist_id, song_id, position)
            VALUES (?, ?, ?)
            """,
            (playlist_id, song_id, next_pos)
        )
        self.conn.commit()
        self.post_playlist_edit_check()

    
    def remove_from_playlist(self, *, song_id: int, playlist_id: int) -> None:
        # next position from DB
        self.cursor.execute(
            """
            DELETE FROM playlist_songs
            WHERE playlist_id = ? AND song_id = ?
            """,
            (playlist_id,song_id)
        )
        self.conn.commit()
        self.post_playlist_edit_check()


    def close(self):
        self.conn.close()

if __name__ == "__main__":
    library = LibraryService("music.db")
    results = library.get_matching_songs("vIVID")
