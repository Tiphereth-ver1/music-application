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