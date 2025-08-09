# youtube.py
import yt_dlp
from platforms import Platform
from pydantic import HttpUrl
from typing import List

class YouTubePlatform(Platform):
    def get_video_formats(self, url: HttpUrl) -> List[dict]:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "skip_download": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["web", "android"],
                    "player_skip": ["configs", "js"],
                }
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(str(url), download=False)
            formats = []
            for f in info.get("formats", []):
                if f.get("ext") not in ["mp4", "mp3"]:
                    continue
                formats.append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("resolution") or "",
                    "fps": f.get("fps"),
                    "filesize": f.get("filesize") or f.get("filesize_approx"),
                    "url": f.get("url"),
                })
            return formats

    def get_audio_formats(self, url: HttpUrl) -> List[dict]:
        return self.get_video_formats(url)  # Similar logic for audio extraction in YouTube
