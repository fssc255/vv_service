from typing import Optional
from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class VideoAddRequest(BaseModel):
    video_id: str
    video_file_path: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
