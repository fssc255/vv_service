from VideoSimilarityAnalyzer import VideoSimilarityAnalyzer
from storages.VectorDbAccessor import VectorDbAccessor
import utils.Logger_example
import numpy as np
import utils.KeyframesSampler_example
from numpy import ndarray
from models.Video import Video
from models.VideoMetadata import VideoMetadata
from storages.IVectorDbAccessor import IVectorDbAccessor
from storages.IDbAccessor import IDbAccessor
from ImageFeatureExtractor import ImageFeatureExtractor
from utils.KeyframesSampler import KeyframesSampler
from VideoMetadataExtractor import VideoMetadataExtractor

# utils.DbAccessor_example.example()
# utils.KeyframesSampler_example.example()
# utils.Logger_example.example()

TEST_FILE1 = R"/mnt/c/Users/11717/Desktop/temp/sample_videos/00078.mp4"
TEST_FILE2 = R"/mnt/c/Users/11717/Desktop/temp/sample_videos/00078-R.mp4"
TEST_FILE2 = R"/mnt/c/Users/11717/Desktop/temp/sample_videos/00069.mp4"


class DumbDbAccessor(IDbAccessor):
    def __init__(self) -> None:
        self.metadataExtractor = VideoMetadataExtractor()

    def get_videos(self) -> list[Video]:
        raise NotImplementedError

    def get_video_metadata(self, video_id: str) -> VideoMetadata | None:
        return {
            "video1": self.metadataExtractor.get_metadata(TEST_FILE1),
            "video2": self.metadataExtractor.get_metadata(TEST_FILE2),
        }[video_id]


class DumbVectorDbAccessor(IVectorDbAccessor):
    def __init__(self) -> None:
        self.featureExtractor = ImageFeatureExtractor()

    def get(self, video_id: str) -> list[ndarray] | None:
        video_file = {
            "video1": TEST_FILE1,
            "video2": TEST_FILE2,
        }[video_id]

        keyframes = KeyframesSampler.sample(video_file, keyframe_count=10)
        fvecs = []
        for keyframe in keyframes:
            fvecs.append(self.featureExtractor.get_feature_vector(keyframe))
        return fvecs

    def add(self, video_id: str, vector: list[ndarray]) -> None:
        raise NotImplementedError

    def delete(self, video_id: str) -> None:
        raise NotImplementedError


va = VideoSimilarityAnalyzer(
    dbAccessor=DumbDbAccessor(),
    vectorDbAccessor=DumbVectorDbAccessor(),
)

print(va.get_similarity("video1", "video2"))
