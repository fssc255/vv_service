from typing import Optional
from pydantic import BaseModel
from models.SimilarVideoGroup import SimilarVideoGroup
from models.VideoMetadata import VideoMetadata


class ApiResponse(BaseModel):
    success: bool
    message: str


class SimilarVideosResponse(ApiResponse):
    data: Optional[list[SimilarVideoGroup]] = None


class VideoAddResponse(ApiResponse):
    data: Optional[VideoMetadata] = None


class VideoRemoveResponse(ApiResponse):
    pass
