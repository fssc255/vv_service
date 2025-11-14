from models.Video import Video
from models.VideoMetadata import VideoMetadata
from storages.IVectorDbAccessor import IVectorDbAccessor
from storages.IDbAccessor import IDbAccessor
from ImageFeatureExtractor import ImageFeatureExtractor
from utils.KeyframesSampler import KeyframesSampler
from VideoMetadataExtractor import VideoMetadataExtractor
import numpy as np


class DumbDbAccessor(IDbAccessor):
    def __init__(self) -> None:
        self.__videos: list[Video] = []
        self.__video_metadata: list[VideoMetadata] = []

    def add_video(self, video: Video) -> None:
        self.__videos.append(video)

    def add_video_metadata(self, video_metadata: VideoMetadata) -> None:
        self.__video_metadata.append(video_metadata)

    def get_videos(self) -> list[Video]:
        return self.__videos

    def get_video_metadata(self, video_id: str) -> VideoMetadata | None:
        for item in self.__video_metadata:
            if item.video_id == video_id:
                return item

        return None


class DumbVectorDbAccessor(IVectorDbAccessor):
    def __init__(self) -> None:
        self.__data: dict[str, list[np.ndarray]] = {}

    def get(self, video_id: str) -> list[np.ndarray] | None:
        return self.__data.get(video_id, None)

    def add(self, video_id: str, vector: list[np.ndarray]) -> None:
        self.__data[video_id] = vector

    def delete(self, video_id: str) -> None:
        self.__data.pop(video_id)
