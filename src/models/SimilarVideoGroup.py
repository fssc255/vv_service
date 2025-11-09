from dataclasses import dataclass


@dataclass
class SimilarVideoGroup:
    reference_video: str
    similar_videos: dict[str, float]
