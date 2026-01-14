from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TYER, TDRC, TCON, COMM, APIC

audio = MP3("beat_it.mp3")
audio.tags               # ID3 object or None
print(audio.keys())             # list of tag keys

# Create tag container if missing
if audio.tags is None:
    audio.add_tags()

audio.tags.add(
    TIT2(encoding=3, text="My Song")
)
audio.tags.add(
    TPE1(encoding=3, text="My Artist")
)

audio.tags.add(
    APIC(encoding=0, data=open("shoot.png").read()))

audio.save()
