from dataclasses import dataclass

@dataclass
class Video:
    id: str
    video_url: str
    cover_url: str
    size: str
    name: str
    uploader: str
    content: str
    record_time: str
    upload_time: str