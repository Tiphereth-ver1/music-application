import yt_dlp
from pathlib import Path
from enum import Enum
from PySide6.QtCore import QObject, QThread, Signal, Slot, QTimer, Qt
from PySide6.QtGui import QPixmap
import uuid
import requests
from collections import deque
from copy import deepcopy
import time, sys
from ...song_subclasses import MP3Song, M4ASong, FLACSong

class DL_OPTIONS(Enum):
    mp3 = "mp3"
    m4a = "m4a"
    flac = "flac"

# This is an exercise in threading. There is a general seperation of concerns with threading that look like the following:
# Job
#

class DownloadJob:
    def __init__(self, url, opt : DL_OPTIONS, video_id: str):
        self.video_id = video_id
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.output_path = base_dir / "music"
        self.url = url
        self.opt = opt
        self.uuid = str(uuid.uuid4())


        codec = {
            DL_OPTIONS.mp3: "mp3",
            DL_OPTIONS.m4a: "m4a",   # note: this typically means AAC in an MP4/M4A container
            DL_OPTIONS.flac: "flac",
        }[opt]

        self.ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        "preferredcodec": codec,

    }],
        'preferredcodec': opt.value,
        "overwrites": True,
        "post_overwrites": True,
        "keepvideo": False,    # Only download the single video URL provided
        'outtmpl': str(self.output_path / '%(id)s.%(ext)s')
        }


## Here is an implementation of a class that uses threading

class PreviewService(QObject):
    update_preview = Signal(dict)
    failed = Signal()

    def __init__(self):
        super().__init__()

    def select_album_art(self, info: dict) -> str | None:
        thumbs = info.get("thumbnails") or []

        # 1) square thumbnails (album art)
        square = [
            t for t in thumbs
            if t.get("width") and t.get("height")
            and t["width"] == t["height"]
        ]

        if square:
            best = max(square, key=lambda t: t["width"])
            print("square")
            return best["url"]

        # 2) fallback: best available thumbnail
        if thumbs:
            best = max(thumbs, key=lambda t: t.get("preference", -100))
            print("normal")
            return best["url"]
        return None


    @Slot(str)
    def extract_preview(self, url):
        print("Dowload starting")
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', None)
                video_id = info.get('id', None)
                video_uploader = info.get('uploader', None)
                thumbnail = self._bytes_from_url(self.select_album_art(info))
                video_duration = info.get('duration_string', None)

                info_package = {
                    "Title" : title, 
                    "ID" : video_id, 
                    "Uploader" : video_uploader,
                    "Thumbnail" : thumbnail,
                    "Duration" : video_duration
                    }

                self.update_preview.emit(info_package)
        except:
            self.failed.emit()
    

    def _bytes_from_url(self, url: str) -> bytes:
        r = requests.get(url, timeout=10)
        thumbnail_bytes = r.content
        return thumbnail_bytes


class DownloadService(QObject):
    progress = Signal(str, dict)   # job_id, payload
    finished = Signal(str, str, str, dict)    # job_id, ext_obj, out_path, dict
    failed = Signal(str, str)      # job_id, error
    idle = Signal()
    update_view = Signal()

    def __init__(self):
        super().__init__()
        self._queue : deque[DownloadJob] = deque()
        self._current : DownloadJob = None
        self._cancel_current = False
        self._last_update = 0
        self._jobs_by_id: dict[str, DownloadJob] = {}


    @Slot(object)
    def enqueue(self, job : DownloadJob):
        self._queue.append(job)
        if self._current is None:
            self._start_next()

    def _start_next(self):
        if not self._queue:
            self._current = None
            self.idle.emit()
            return
        self._current = self._queue.popleft()
        self._cancel_current = False
        self._run_current_job()
        self._last_update = 0
    
    def _run_current_job(self):
        job = self._current
        job_id = job.uuid
        self._jobs_by_id[job_id] = job

        def hook(d):
            self._hook_for_job(job_id, d)
        
        def post_hook(d):
            self._post_hook_for_job(job_id, d)

        opts = deepcopy(job.ydl_opts)
        opts["progress_hooks"] = [hook]
        opts["postprocessor_hooks"] = [post_hook]
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self._current.url])
        except Exception as e:
            self.failed.emit(job_id, str(e))
        finally:
            self._jobs_by_id.pop(job_id, None)
            self._current = None
            QTimer.singleShot(50, self._start_next)  # instead of calling directly

    
    def _hook_for_job(self, job_id: str, d):
        status = d.get("status")

        if status == "downloading":
            # Throttling hook calls so stuff doesn't explode
            now = time.monotonic()
            if now - self._last_update < 0.05:   # 10 Hz
                return
            self._last_update = now

            downloaded = d.get("downloaded_bytes") or 0
            downloaded_str = f"{downloaded/1024/1024:,.2f} MiB" if downloaded else " ? "

            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            total_str = f"{total/1024/1024:,.2f} MiB" if total else " ? "
            pct = f"{(downloaded/total*100):5.1f}%" if total else " ? %"

            spd = d.get("speed")
            spd_str = f"{spd/1024/1024:,.2f} MiB/s" if spd else " ? "

            eta = d.get("eta")
            eta_str = str(eta) if eta is not None else "?"


            self.progress.emit(job_id,{
                "Downloaded": downloaded_str,
                "Percentage": pct,
                "Total": total_str,
                "Speed": spd_str,
                "ETA": eta_str,
            })

        elif status == "error":
            self.failed.emit(job_id, "download error")
            
    def _post_hook_for_job(self, job_id: str, d: dict):
        if d.get("status") != "finished":
            return

        pp = str(d.get("postprocessor") or "")

        if "ExtractAudio" not in pp and "MoveFiles" not in pp:
            return

        job = self._jobs_by_id.get(job_id)
        info = d.get("info_dict") or {}

        info_parse = {
                "ID": info.get("id"),
                "Title": info.get("title"),
                "Uploader": info.get("uploader"),
                "Artist" : info.get("artist"),
                "Title" : info.get("title"),
                "Album" : info.get("album"),
            }

        # Choose video id: prefer job.video_id, fallback to hook info_dict
        vid = (job.video_id if job else None) or info.get("ID")
        if not vid:
            self.failed.emit(job_id, f"No video id; cannot resolve output path. pp={pp}")
            return

        final_ext = (job.opt.value if job else "mp3")

        out_path = (job.output_path if job else Path.cwd()) / f"{vid}.{final_ext}"

        # Windows latency / move guard
        for _ in range(50):  # ~2.5s
            if out_path.exists():
                self.finished.emit(job_id, final_ext, str(out_path), info_parse)
                return
            time.sleep(0.05)

        self.failed.emit(job_id, f"Expected output not found: {out_path} (pp={pp})")

        print(info)



class DownloadManager(QObject):
    request_job = Signal(DownloadJob)
    request_preview = Signal(str)
    download_status = Signal(dict)
    updating_view = Signal()
    return_preview = Signal(object)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.download_service = DownloadService()
        self.preview_service = PreviewService()
        # Initialise thread for runnning
        self.download_thread = QThread()
        self.preview_thread = QThread()
        self.preview_bytes_dict = {}
        self.processed_songs = []
        self.last_preview_video_id = None
        self.preview_url = None
        self.automatic_metadata = True

        # Moves the runtime of the service to the thread and starts it
        self.download_service.moveToThread(self.download_thread)
        self.preview_service.moveToThread(self.preview_thread)

        self.request_job.connect(self.download_service.enqueue)
        self.request_preview.connect(self.preview_service.extract_preview)
        self.download_service.progress.connect(self.request_status)
        self.download_service.finished.connect(self.write_metadata)
        self.download_service.finished.connect(lambda *args: print("FINISHED SIGNAL:", args))
        self.download_service.failed.connect(lambda job_id, err: print("FAILED", job_id, err))
        self.preview_service.failed.connect(lambda *args, err: print("FAILED", err))

        # self.download_service.update_view.connect(self.update_view)
        self.preview_service.update_preview.connect(self.relay_preview)

        self.download_thread.start()
        self.preview_thread.start()
    
    def request_enqueue(self, url : str, opt: DL_OPTIONS = DL_OPTIONS.mp3):
        if url.startswith("https://www.youtube.com") or url.startswith("https://music.youtube.com"):
            vid = self.last_preview_video_id  # best if preview was run for this URL
            job = DownloadJob(url, opt, video_id=vid)
            self.request_job.emit(job)

        else:
            print("Invalid link")
    
    def preview_song(self, url : str):
        if url.startswith("https://www.youtube.com") or url.startswith("https://music.youtube.com"):
            self.request_preview.emit(url)
            print("Song download requested")
        else:
            print("Invalid link")
    
    def relay_preview(self, info : dict):
        self.return_preview.emit(info)
        self.last_preview_video_id = info.get("ID")
        self.preview_bytes_dict[self.last_preview_video_id] = info.get("Thumbnail")
    
    def song_select(self, filepath, final_ext):
        if final_ext == "mp3":
            song = MP3Song(filepath)
        elif final_ext == "m4a":
            song = M4ASong(filepath)
        elif final_ext == "flac":
            song = FLACSong(filepath)
        return song

    @Slot(str, str, dict) 
    def write_metadata(self, job_id, final_ext, filepath, info):
        print(final_ext)
        print("metadata written")
        if not self.automatic_metadata:
            self.updating_view.emit()
            return
        
        if job_id not in self.processed_songs:
            song = self.song_select(filepath, final_ext)
            print(filepath)

            song.update(
                artist=info.get("Artist") or info.get("Uploader"),
                title=info.get("Title"),
                album=info.get("Album"),
            )

            song.rename_file()

            art_bytes = self.preview_bytes_dict[info.get("ID")]
            if art_bytes:
                song.set_art_bytes(True, art_bytes)
            self.updating_view.emit()
            self.processed_songs.append(job_id)

    @Slot(str, dict)
    def request_status(self, job_id: str, d: dict) -> None:
        '''
        Docstring for request_status
        
        :param self: Description
        :param job_id: Description
        :type job_id: str
        :param d: Description
        :type d: dict
        :return: Returns a tuple with the following structure:
        - job id
        - percentage download
        - download speed
        - filename
        - eta
        :rtype: tuple[str, str, str, str, str]
        '''

        self.download_status.emit(d)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    downloadManager = DownloadManager()
    downloadManager.request_enqueue("https://www.youtube.com/watch?v=gE7SmrBmXsg")
    downloadManager.request_enqueue('https://www.youtube.com/watch?v=-NEGsRc3fbA')

    sys.exit(app.exec())
