import numpy as np
from storages.IDbAccessor import IDbAccessor
from storages.IVectorDbAccessor import IVectorDbAccessor
from utils.Logger import Logger
from VectorsSimilarityCalculator import VectorsSimilarityCalculator


class VideoSimilarityAnalyzer:
    def __init__(self, dbAccessor: IDbAccessor, vectorDbAccessor: IVectorDbAccessor) -> None:
        self.__db_accessor = dbAccessor
        self.__vector_db_accessor = vectorDbAccessor
        self.__similarity_calculator = VectorsSimilarityCalculator()

    def get_similarity(self, video1_id: str, video2_id: str) -> float:
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

        metadata_similarity = self.__calculate_metadata_similarity(video1_id, video2_id)
        if metadata_similarity < 0:
            return 0
        elif metadata_similarity > 1:
            return 1

        semantics_similarity = self.__calculate_semantics_similarity(video1_id, video2_id)
        if metadata_similarity < 0:
            return 0

        comprehensive_similarity = metadata_similarity * 0.3 + semantics_similarity * 0.7

        Logger.info(
            f"({video1_id}, {video2_id}) 元数据相似度: {metadata_similarity:.3f}, 语义相似度: {semantics_similarity:.3f}, 综合相似度: {comprehensive_similarity:.3f}")

        return comprehensive_similarity

    def __calculate_metadata_similarity(self, video1_id: str, video2_id: str) -> float:
        video1_metadata = self.__db_accessor.get_video_metadata(video1_id)
        if video1_metadata is None:
            Logger.error(f"无法获取Id为{video1_id}的视频的元数据")
            return 0

        video2_metadata = self.__db_accessor.get_video_metadata(video2_id)
        if video2_metadata is None:
            Logger.error(f"无法获取Id为{video2_id}的视频的元数据")
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

    def __calculate_semantics_similarity(self,  video1_id: str, video2_id: str) -> float:
        def get_or_add_video_feature_vector(video_id: str) -> list[np.ndarray] | None:
            return self.__vector_db_accessor.get(video_id)

        video1_feature_vector = get_or_add_video_feature_vector(video1_id)
        if video1_feature_vector is None:
            Logger.error(f"无法获取视频的特征向量 (VideoId={video1_id})")
            return -1

        video2_feature_vector = get_or_add_video_feature_vector(video2_id)
        if video2_feature_vector is None:
            Logger.error(f"无法获取视频的特征向量 (VideoId={video1_id})")
            return -1

        return self.__similarity_calculator.calculate(video1_feature_vector, video2_feature_vector)
