from pathlib import Path
from song import Song

def filepath_to_songs():
    base_dir = Path(__file__).resolve().parent.parent
    music_folder = base_dir / "music"
    songs = []
    for file_path in music_folder.rglob("*.mp3"):
        print(file_path)
        rel_path = file_path.relative_to(base_dir)
        songs.append(Song(rel_path))
    return songs

