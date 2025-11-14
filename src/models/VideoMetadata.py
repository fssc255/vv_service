from typing import Optional
from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class VideoMetadata(BaseModel):
    id: int
    video_id: str
    width: Optional[int]
    height: Optional[int]
    fps: Optional[float]
    duration: Optional[int]
    file_type: str
    file_size: int
    create_time: int
    modify_time: int
    md5: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
