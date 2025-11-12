from typing import Optional
from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class VARequest(BaseModel):
    action: str
    video_id: Optional[str] = None
    video_file_path: Optional[str] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True
