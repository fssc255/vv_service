import numpy as np
from storages.IDbAccessor import IDbAccessor
from storages.IVectorDbAccessor import IVectorDbAccessor
from utils.Logger import Logger
from utils.VectorsSimilarityCalculator import VectorsSimilarityCalculator
from utils.VideoMetadataExtractor import VideoMetadataExtractor
from utils.VideoFeatureVectorsExtractor import VideoFeatureVectorsExtractor
from models.tables.Video import Video


class VideoSimilarityAnalyzer:
    def __init__(self) -> None:
        self.__video_feature_vectors_extractor = VideoFeatureVectorsExtractor()
        self.__video_metadata_extractor = VideoMetadataExtractor()

    def get_similarity(self, video1: Video, video2: Video) -> float:
        """
        获取两个视频的相似度

        Args:
            video_id_a (str): 第一个视频的唯一标识符
            video_id_b (str): 第二个视频的唯一标识符

        Returns:
            float: 视频相似度得分，范围在[0,1]之间，值越高相似度越高

        Raises:
            InvalidVideoIdError: 当输入的 video_id 在数据库中不存在时抛出
            Error: 其他错误
        """

        metadata_similarity = self.__calculate_metadata_similarity(video1, video2)
        if metadata_similarity < 0:
            return 0
        elif metadata_similarity > 1:
            Logger.info(f"({video1.id}, {video2.id}) MD5 相同")
            return 1

        semantics_similarity = self.__calculate_semantics_similarity(video1, video2)
        if semantics_similarity < 0:
            return 0

        comprehensive_similarity = metadata_similarity * 0.3 + semantics_similarity * 0.7

        Logger.info(
            f"({video1.id}, {video2.id}) 元数据相似度: {metadata_similarity:.3f}, 语义相似度: {semantics_similarity:.3f}, 综合相似度: {comprehensive_similarity:.3f}")

        return max(comprehensive_similarity, 0)

    def __calculate_metadata_similarity(self, video1: Video, video2: Video) -> float:
        video1_metadata = self.__video_metadata_extractor.get_metadata(video1.file_path)
        if video1_metadata is None:
            Logger.error(f"无法获取视频的元数据 (VideoId={video1.id})")
            return 0

        video2_metadata = self.__video_metadata_extractor.get_metadata(video2.file_path)
        if video2_metadata is None:
            Logger.error(f"无法获取视频的元数据 (VideoId={video2.id})")
            return 0

        if video1_metadata.md5 == video2_metadata.md5:
            return 2

        data1 = np.array((
            video1_metadata.width,
            video1_metadata.height,
            video1_metadata.fps,
            video1_metadata.duration,
        ))
        data2 = np.array((
            video2_metadata.width,
            video2_metadata.height,
            video2_metadata.fps,
            video2_metadata.duration,
        ))

        return sum(np.vectorize(lambda x, y: min(x, y) / max(x, y))(data1, data2) * (0.01, 0.01, 0.18, 0.8))

    def __calculate_semantics_similarity(self, video1: Video, video2: Video) -> float:
        video1_feature_vector = self.__video_feature_vectors_extractor.get_feature_vectors(video1.file_path)
        if video1_feature_vector is None:
            Logger.error(f"无法获取视频的特征向量 (VideoId={video1.id})")
            return -1

        video2_feature_vector = self.__video_feature_vectors_extractor.get_feature_vectors(video2.file_path)
        if video2_feature_vector is None:
            Logger.error(f"无法获取视频的特征向量 (VideoId={video2.id})")
            return -1

        return VectorsSimilarityCalculator.calculate(video1_feature_vector, video2_feature_vector)
