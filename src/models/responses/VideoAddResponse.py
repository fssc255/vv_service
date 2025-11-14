from typing import Optional
from models.VideoMetadata import VideoMetadata
from models.responses.ApiResponse import ApiResponse


class VideoAddResponse(ApiResponse):
    data: Optional[VideoMetadata] = None