from dataclasses import dataclass
from IVideoAnalyzer import IVideoAnalyzer


class SimilarVideoGroup:
    reference_video: str
    similar_videos: dict[str, float]


class SimilarVideosSearcher:
    @staticmethod
    def find_similar_videos(videoAnalyzer: IVideoAnalyzer, threshold: float) -> list[SimilarVideoGroup]:
        
        return []
