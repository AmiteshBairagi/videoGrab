# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from youtube import YouTubePlatform
from instagram import InstagramPlatform
from platforms import Platform

# Request model
class VideoRequest(BaseModel):
    url: HttpUrl
    platform: str  # This allows the user to select platform (youtube/instagram)
    format: str    # This allows the user to select mp3/mp4

# Response models
class FormatInfo(BaseModel):
    format_id: str
    ext: str
    resolution: str
    fps: int | None
    filesize: int | None
    url: str

class VideoResponse(BaseModel):
    title: str
    formats: list[FormatInfo]

app = FastAPI()

# Platform mapping (easy to extend for more platforms)
PLATFORM_MAP = {
    "youtube": YouTubePlatform(),
    "instagram": InstagramPlatform(),
}

@app.post("/get-download-links", response_model=VideoResponse)
async def get_download_links(video_req: VideoRequest):
    platform = PLATFORM_MAP.get(video_req.platform.lower())
    if not platform:
        raise HTTPException(status_code=400, detail="Unsupported platform")

    try:
        # Fetch formats based on user choice (mp3 or mp4)
        if video_req.format == "mp3":
            formats = platform.get_audio_formats(video_req.url)
        elif video_req.format == "mp4":
            formats = platform.get_video_formats(video_req.url)
        else:
            raise HTTPException(status_code=400, detail="Invalid format selected")

        if not formats:
            raise HTTPException(status_code=404, detail="No downloadable formats found.")

        return {
            "title": "Sample Title",  # This could be dynamic based on platform
            "formats": formats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
