# platforms.py
from abc import ABC, abstractmethod
from pydantic import HttpUrl
from typing import List

class Platform(ABC):
    @abstractmethod
    def get_video_formats(self, url: HttpUrl) -> List[dict]:
        pass

    @abstractmethod
    def get_audio_formats(self, url: HttpUrl) -> List[dict]:
        pass
