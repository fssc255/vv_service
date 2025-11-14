from typing import Optional
from models.SimilarVideoGroup import SimilarVideoGroup
from models.responses.ApiResponse import ApiResponse


class SimilarVideosResponse(ApiResponse):
    data: Optional[list[SimilarVideoGroup]] = None