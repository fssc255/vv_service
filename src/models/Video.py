from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class Video(BaseModel):
    id: str
    video_url: str
    cover_url: str
    size: str
    name: str
    uploader: str
    content: str
    record_time: str
    upload_time: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
