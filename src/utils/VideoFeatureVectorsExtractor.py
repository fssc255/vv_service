import os
from typing import Optional
from models.tables.Video import Video
from utils.ImageFeatureExtractor import ImageFeatureExtractor
from utils.KeyframesSampler import KeyframesSampler
from utils.Logger import Logger
import numpy as np


class VideoFeatureVectorsExtractor:
    def __init__(self) -> None:
        self.__image_feature_extractor = ImageFeatureExtractor()
        self.__cache: dict[str, Optional[list[np.ndarray]]] = {}

    def get_feature_vectors(self, video_file_path: str) -> Optional[list[np.ndarray]]:
        if not os.path.exists(video_file_path):
            raise FileNotFoundError(video_file_path)

        if video_file_path in self.__cache:
            return self.__cache[video_file_path]

        feature_vectors = self.__get_feature_vectors(video_file_path)
        self.__cache[video_file_path] = feature_vectors

        return feature_vectors

    def __get_feature_vectors(self, video_file_path: str) -> Optional[list[np.ndarray]]:
        try:
            Logger.info(f"采样视频关键帧 (File={video_file_path})")
            keyframes = KeyframesSampler.sample(video_file_path, 10)
        except Exception as e:
            Logger.error(f"无法采样视频的关键帧 (File=`{video_file_path}`, Error={e})")
            return None

        try:
            Logger.info(f"计算视频关键帧特征向量 (File={video_file_path})")
            return [self.__image_feature_extractor.get_feature_vector(x) for x in keyframes]
        except Exception as e:
            Logger.error(f"从视频的关键帧中提取特征向量时发生错误 (File=`{video_file_path}`, Error={e})")
            return None
