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
from ...library_manager import LibraryService
import logging

max_info_length = 90

class DL_OPTIONS(Enum):
    mp3 = "mp3"
    m4a = "m4a"
    flac = "flac"

# This is an exercise in threading. There is a general seperation of concerns with threading that look like the following:

def _bytes_from_url(url: str) -> bytes:
    r = requests.get(url, timeout=10)
    thumbnail_bytes = r.content
    return thumbnail_bytes

def select_album_art(info: dict) -> str | None:
    thumbs = info.get("thumbnails") or []
    print(thumbs)

    # 1) square thumbnails (album art)
    square = [
        t for t in thumbs
        if t.get("width") and t.get("height")
        and t["width"] == t["height"]
    ]

    if square:
        best = max(square, key=lambda t: t["width"])
        logging.debug("Square chosen")
        return best["url"]

    # 2) fallback: best available thumbnail
    if thumbs:
        best = max(thumbs, key=lambda t: t.get("preference", -100))
        logging.debug("Thumb chosen")

        return best["url"]
    
    logging.debug("No thumbnail could be selected")
    return None



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
    update_playlist_preview = Signal(dict)
    failed = Signal()

    def __init__(self):
        super().__init__()
    
    @Slot(str)
    def extract_playlist_preview(self, url):
        ydl_opts = {
                "quiet": True,
                "extract_flat": True, 
                "skip_download": True,
                "js_runtimes": {"deno": {}},   # or {"node": {}}

            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            entries = info.get("entries") or []
            id_dict = {}
            for i, e in enumerate(entries, start=1):
                title = e.get("title")
                video_id = e.get("id")
                uploader = e.get("uploader")
                duration = e.get("duration")

                u = e.get("webpage_url") or e.get("original_url")
                if not u and video_id:
                    u = f"https://www.youtube.com/watch?v={video_id}"

                if video_id and u:
                    id_dict[video_id] = {
                        "Index": i,
                        "Link": u,
                        "Title": title,
                        "Uploader": uploader,
                        "Duration": duration,
                    }

            self.update_playlist_preview.emit(id_dict)


    @Slot(str)
    def extract_preview(self, url):
        logging.debug("Dowload starting")
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
                thumb_url = select_album_art(info)
                thumbnail = _bytes_from_url(thumb_url) if thumb_url else None
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
        self._job_ids : set = set()


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
            eta_str = f'{str(eta)} seconds' if eta is not None else "?"
        
            info_dict = d.get("info_dict")
            download_info = f"Currently downloading {info_dict['title']} - {info_dict["uploader"]}"[:max_info_length]

            self.progress.emit(job_id,{
                "Downloaded": downloaded_str,
                "Percentage": pct,
                "Total": total_str,
                "Speed": spd_str,
                "ETA": eta_str,
                "Information" : download_info
            })

        elif status == "error":
            self.failed.emit(job_id, "download error")
            logging.exception("Error encountered during download")
        
            info_dict = d.get("info_dict")
            download_info = f"Failed download for {info_dict['title']} - {info_dict["uploader"]}"[:max_info_length]

            self.progress.emit(job_id,{
                "Information" : download_info
            })

            return

            
    def _post_hook_for_job(self, job_id: str, d: dict):
        if d.get("status") != "finished":
            logging.debug("Attempted post-hook")
        
            info_dict = d.get("info_dict")
            download_info = f"Processing {info_dict['title']} - {info_dict["uploader"]}"[:max_info_length]

            self.progress.emit(job_id,{
                "Percentage": '100%',
                "ETA": 0,
                "Information" : download_info
            })

            return

        pp = str(d.get("postprocessor") or "")

        if "MoveFiles" not in pp:
            return

        job = self._jobs_by_id.get(job_id)
        info = d.get("info_dict") or {}
        final_job_id = f"{job_id} : {info.get("id")}"

        if final_job_id in self._job_ids:
            logging.error("Attempted duplicate hook")
            return

        # Choose video id: prefer job.video_id, fallback to hook info_dict
        vid = (job.video_id if job else None) or info.get("id")
        if not vid:
            self.failed.emit(job_id, f"No video id; pp={pp}")
            return

        final_ext = job.opt.value if job else "mp3"
        out_path = (job.output_path if job else Path.cwd()) / f"{vid}.{final_ext}"

        key = str(out_path)
        if key in self._job_ids:
            return
        self._job_ids.add(key)  # mark immediately/ f"{vid}.{final_ext}"

        # Windows latency / move guard
        try:
            for _ in range(50):
                if out_path.exists():
                    info_parse = {
                        "ID": vid,
                        "Title": info.get("title"),
                        "Uploader": info.get("uploader"),
                        "Thumbnail": _bytes_from_url(select_album_art(info)),
                        "Artist": info.get("artist") or info.get("uploader"),
                        "Album": info.get("album"),
                    }
                    final_job_id = f"{job_id} : {vid}"
                    self.finished.emit(final_job_id, final_ext, str(out_path), info_parse)
                    download_info = f"Finished {info['title']} - {info["uploader"]}"[:max_info_length]
                    self.progress.emit(job_id,{
                        "Information" : download_info
                    })
                    return
                time.sleep(0.05)

            self._job_ids.discard(key)  # allow retry if move latency exceeded
            self.failed.emit(job_id, f"Expected output not found: {out_path} (pp={pp})")

        except Exception:
            self._job_ids.discard(key)
            raise



class DownloadManager(QObject):
    request_job = Signal(DownloadJob)
    request_preview = Signal(str)
    request_playlist_preview = Signal(str)
    download_status = Signal(dict)
    updating_view = Signal()
    return_preview = Signal(object)
    return_playlist_preview = Signal(dict)

    def __init__(self, library : LibraryService, parent = None):
        super().__init__(parent)
        self.download_service = DownloadService()
        self.preview_service = PreviewService()
        # Initialise thread for runnning
        self.download_thread = QThread()
        self.preview_thread = QThread()
        self.last_preview_video_id = None
        self.last_playlist = dict()
        self.processed_song_ids = set()
        self.preview_url = None
        self.automatic_metadata = True
        self.lib = library

        # Moves the runtime of the service to the thread and starts it
        self.download_service.moveToThread(self.download_thread)
        self.preview_service.moveToThread(self.preview_thread)

        self.request_job.connect(self.download_service.enqueue)
        self.request_preview.connect(self.preview_service.extract_preview)
        self.request_playlist_preview.connect(self.preview_service.extract_playlist_preview)
        self.download_service.progress.connect(self.request_status)
        self.download_service.finished.connect(self.write_metadata)
        self.download_service.finished.connect(lambda *args: logging.info("FINISHED SIGNAL:", args))
        self.download_service.failed.connect(lambda job_id, err: logging.error("FAILED", job_id, err))
        self.preview_service.failed.connect(lambda: logging.error("PREVIEW FAILED"))
        self.preview_service.update_playlist_preview.connect(self.relay_playlist_preview)

        # self.download_service.update_view.connect(self.update_view)
        self.preview_service.update_preview.connect(self.relay_preview)

        self.download_thread.start()
        self.preview_thread.start()
            
    def classify_input(self, url : str) -> None:
        if 'playlist' in url:
            self.playlist_preview(url)
            logging.debug("playlist mode selected")
        else:
            self.preview_song(url)
            logging.debug("single mode selected")

    def request_enqueue(self, url : str, opt: DL_OPTIONS = DL_OPTIONS.mp3, vid = None):
        if url.startswith("https://www.youtube.com") or url.startswith("https://music.youtube.com"):
            if not vid:
                vid = self.last_preview_video_id  # best if preview was run for this URL
            job = DownloadJob(url, opt, video_id=vid)
            self.request_job.emit(job)

        else:
            logging.error("Invalid link")
    
    def batch_request_enqueue(self,  opt : DL_OPTIONS = DL_OPTIONS.mp3):
        logging.info(self.last_playlist)
        for id, info_dict in self.last_playlist.items():
            logging.info(opt,id)
            job = DownloadJob(info_dict["Link"], opt, id)
            self.request_job.emit(job)

    def preview_song(self, url : str):
        if url.startswith("https://www.youtube.com") or url.startswith("https://music.youtube.com"):
            self.request_preview.emit(url)
            logging.debug("Song preview requested")
        else:
            logging.error("Invalid link")
    
    def playlist_preview(self, url : str):
        if url.startswith("https://www.youtube.com") or url.startswith("https://music.youtube.com"):
            self.request_playlist_preview.emit(url)
    
    def relay_preview(self, info : dict):
        self.return_preview.emit(info)
        self.last_preview_video_id = info.get("ID")
    
    @Slot(dict)
    def relay_playlist_preview(self, infodict : dict):
        logging.debug("playlist preview relayed")
        self.last_playlist.clear()
        self.last_playlist = infodict
        self.return_playlist_preview.emit(infodict)
    
    def song_select(self, filepath, final_ext):
        if final_ext == "mp3":
            song = MP3Song(filepath)
        elif final_ext == "m4a":
            song = M4ASong(filepath)
        elif final_ext == "flac":
            song = FLACSong(filepath)
        return song

    @Slot(str, str, str, dict)
    def write_metadata(self, job_id, final_ext, filepath, info) -> None:
        '''
        Handles creation of song objects and metadata writing after worker thread finishes downloading song.
        Writes artist, title and album automatically based on info passed from the worker thread. \n

        Args:
            :param self: 
            :param job_id: Job ID associated with the download
            :type: str
            :param final_ext: extension of intended output file
            :type: str
            :param filepath: Location to the filepath for the song to be written to
            :type: str 
            :param info: Object containing metadata to be provided to the song
            :type: dict \n
    
        '''
        start = round(time.time()*1000)
        logging.debug("WRITE_METADATA:", job_id, info.get("ID"), filepath, final_ext)
        if not self.automatic_metadata:
            self.updating_view.emit()
            return
        
        song = self.song_select(Path(filepath), final_ext)
        end1 = round(time.time()*1000)

        song.update(
            artist=info.get("Artist") or info.get("Uploader"),
            title=info.get("Title"),
            album=info.get("Album"),
        )

        end2 = round(time.time()*1000)

        art_bytes = info.get("Thumbnail")
        if art_bytes:
            song.set_art_bytes(True, art_bytes)
            del art_bytes  # drop reference immediately
        
        end3 = round(time.time()*1000)

        path = song.rename_file()

        self.lib.upsert_song_from_path(path)
        self.lib.post_album_add_check()
        end = round(time.time()*1000)
        logging.info(f'''
        Metadata Writing Stats \n
        ----------------------
        Creating Song Object : {end1 - start} \n
        Writing Text Metadata : {end2 - end1} \n
        Writing Art Bytes to Song : {end3 - end2} \n
        Upsert Song to Database : {end - end3} \n
        Total time : {end - start} 
        '''
        )

    @Slot(str, dict)
    def request_status(self, job_id: str, d: dict) -> None:
        '''        
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
    downloadManager.playlist_preview("https://www.youtube.com/playlist?list=OLAK5uy_ksdxJNHsGSstuGy75Q6460PqGRg1lxbks")

    sys.exit(app.exec())
