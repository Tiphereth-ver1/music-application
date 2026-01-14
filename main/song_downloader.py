import yt_dlp
from pathlib import Path
from enum import Enum
from PySide6.QtCore import QObject, QThread, Signal, Slot, QTimer
import uuid
from collections import deque
from copy import deepcopy
import time, sys

class DL_OPTIONS(Enum):
    mp3 = "mp3"
    m4a = "m4a"

# This is an exercise in threading. There is a general seperation of concerns with threading that look like the following:
# Job
#

class DownloadJob:
    def __init__(self, url, opt : DL_OPTIONS):
        base_dir = Path(__file__).resolve().parent.parent
        self.output_path = base_dir / "music"
        self.url = url
        self.uuid = str(uuid.uuid4())
        self.ydl_opts = {
        'format': f'{opt.value}/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
        'preferredcodec': opt.value,
        'noplaylist': True,    # Only download the single video URL provided
        'outtmpl': str(self.output_path / '%(title)s.%(ext)s')
        }


## Here is an implementation of a class that uses threading

class DownloadService(QObject):
    progress = Signal(str, dict)   # job_id, payload
    finished = Signal(str)    # job_id
    failed = Signal(str, str)      # job_id, error
    idle = Signal()

    def __init__(self):
        super().__init__()
        self._queue : deque[DownloadJob] = deque()
        self._current : DownloadJob = None
        self._cancel_current = False
        self._last_update = 0

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
        self.last_update = 0


    def _run_current_job(self):
        job = self._current
        job_id = job.uuid

        def hook(d):
            self._hook_for_job(job_id, d)

        opts = deepcopy(job.ydl_opts)
        opts["progress_hooks"] = [hook]

        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self._current.url])
        except Exception as e:
            self.failed.emit(job_id, str(e))
        finally:
            self._current = None
            QTimer.singleShot(50, self._start_next)  # instead of calling directly

    
    def _hook_for_job(self, job_id: str, d):
        status = d.get("status")

        if status == "downloading":
            # Throttling hook calls so stuff doesn't explode
            now = time.monotonic()
            if now - self._last_update < 0.1:   # 10 Hz
                return
            self._last_update = now

            self.progress.emit(job_id,{
                "percent": d.get("_percent_str"),
                "speed": d.get("_speed_str"),
                "eta": d.get("eta"),
                "filename": d.get("filename"),
            })

            pct = d.get("_percent_str") or "?"
            spd = d.get("_speed_str") or "?"
            eta = d.get("_eta_str") or (str(d.get("eta")) if d.get("eta") is not None else "?")
            fn  = d.get("filename") or d.get("tmpfilename") or ""

            # carriage return keeps it on one updating line
            sys.stdout.write(f"\r[{job_id[:6]}] {pct} {spd} ETA {eta} {fn[:60]}")
            sys.stdout.flush()

        elif status == "error":
            self.failed.emit(job_id, "download error")
        
        elif status == "finished":
            sys.stdout.write("\nDownload finished; postprocessing...\n")
            sys.stdout.flush()
            self.finished.emit(job_id)



        # blocking yt-dlp call here
        # emit progress via hooks
        # on completion: emit finished/failed then call _start_next()
        ...
        

class DownloadManager(QObject):
    request_job = Signal(DownloadJob)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.download_service = DownloadService()
        # Initialise thread for runnning
        self.download_thread = QThread()

        # Moves the runtime of the service to the thread and starts it
        self.download_service.moveToThread(self.download_thread)
        self.download_thread.start()
        self.request_job.connect(self.download_service.enqueue)
    
    def request_enqueue(self, url : str, opt: DL_OPTIONS = DL_OPTIONS.mp3):
        job = DownloadJob(url, opt)
        self.request_job.emit(job)    
    


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    downloadManager = DownloadManager()

    last_update = 0
    now = time.monotonic()
    if now - last_update < 0.1:   # 10 Hz
        return

    downloadManager.request_enqueue("https://www.youtube.com/watch?v=tZCz7fUpygg")
    downloadManager.request_enqueue('https://www.youtube.com/watch?v=-NEGsRc3fbA')

    sys.exit(app.exec())
