from typing import Optional
from dataclasses import dataclass


@dataclass
class VideoMetadata:
    width: Optional[int]
    height: Optional[int]
    fps: Optional[float]
    duration: Optional[int]
    file_type: str
    file_size: int
    create_time: int
    modify_time: int
    md5: str
