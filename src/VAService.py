import os
from typing import Optional
from VideoSimilarityAnalyzer import VideoSimilarityAnalyzer
from models.VideoMetadata import VideoMetadata
from storages.DbAccessor import DbAccessor
from storages.VectorDbAccessor import VectorDbAccessor
from models.Video import Video
from models.SimilarVideoGroup import SimilarVideoGroup
from storages.IDbAccessor import IDbAccessor
from storages.IVectorDbAccessor import IVectorDbAccessor
from VideoMetadataExtractor import VideoMetadataExtractor
from ImageFeatureExtractor import ImageFeatureExtractor
from utils.KeyframesSampler import KeyframesSampler
from utils.Logger import Logger


class VAService:
    def __init__(self) -> None:
        # 使用真实的数据库访问器
        db_accessor = DbAccessor()
        vector_db_accessor = VectorDbAccessor()

        self.__image_feature_extractor = ImageFeatureExtractor()
        self.__db_accessor: IDbAccessor = db_accessor
        self.__vector_db_accessor: IVectorDbAccessor = vector_db_accessor

    def extract_image_embedding(self, image_array) -> list:
        """提取图像特征向量（供外部API调用）"""
        vector = self.__image_feature_extractor.get_feature_vector(image_array)
        return vector.tolist()

    def add_video(self, video_id: str, video_file_path: str) -> Optional[VideoMetadata]:
        if not os.path.exists(video_file_path) or os.path.isdir(video_file_path):
            Logger.info(f"视频文件不存在 (File={video_file_path})")
            raise FileNotFoundError(video_file_path)

        # 1.获取视频元数据
        try:
            Logger.info(f"获取视频元数据 (File={video_file_path})")
            video_metadata = VideoMetadataExtractor.get_metadata(video_file_path)
            video_metadata.video_id = video_id
        except Exception as e:
            Logger.error(f"无法获取视频的元数据 (File=`{video_file_path}`, Error={e})")
            return None

        # 2.采样关键帧，计算特征向量并添加到向量数据库
        try:
            Logger.info(f"采样视频关键帧 (File={video_file_path})")
            keyframes = KeyframesSampler.sample(video_file_path, 10)
        except Exception as e:
            Logger.error(f"无法提取视频的关键帧 (File=`{video_file_path}`, Error={e})")
            return None

        try:
            Logger.info(f"计算视频关键帧特征向量 (File={video_file_path})")
            feature_vectors = [self.__image_feature_extractor.get_feature_vector(x) for x in keyframes]
            self.__vector_db_accessor.add(video_id, feature_vectors)
        except Exception as e:
            Logger.error(f"从视频的关键帧中提取特征向量时发生错误 (File=`{video_file_path}`, Error={e})")
            return None

        # TODO: 记得删，实际数据添加靠上级后端（已经由Go后端管理）
        # self.__db_accessor.add_video(...)
        # self.__db_accessor.add_video_metadata(...)

        return video_metadata

    def delete_video(self, video_id: str) -> bool:
        try:
            self.__vector_db_accessor.delete(video_id)
            return True
        except Exception as e:
            Logger.error(f"从向量数据库中删除 {video_id} 时发生错误 (Error={e})")
            return False

    def find_similar_videos(self, threshold: float) -> list[SimilarVideoGroup]:
        video_similarity_analyzer = VideoSimilarityAnalyzer(
            dbAccessor=self.__db_accessor,
            vectorDbAccessor=self.__vector_db_accessor,
        )

        videos = self.__db_accessor.get_videos()

        compare_cache: dict[str, float] = {}
        processed_video_id_set: set[str] = set()
        similar_group_list: list[SimilarVideoGroup] = []

        # 1.筛选相似组
        for reference_video in videos:
            # 跳过已处理
            if reference_video.id in processed_video_id_set:
                continue

            processed_video_id_set.add(reference_video.id)

            similar_group = SimilarVideoGroup(
                reference_video=reference_video.id,
                similar_videos={}
            )
            for test_video in videos:
                # 跳过自比较
                if reference_video.id == test_video.id:
                    continue

                # 跳过已处理
                if test_video.id in processed_video_id_set:
                    continue

                if reference_video.id < test_video.id:
                    first_video, second_video = reference_video, test_video
                else:
                    first_video, second_video = test_video, reference_video

                # 先尝试从缓存中获取，没有再调用分析器
                cache_id = f"{first_video.id}:{second_video.id}"
                if cache_id in compare_cache:
                    similarity = compare_cache[cache_id]
                else:
                    similarity = video_similarity_analyzer.get_similarity(first_video.id, second_video.id)
                    compare_cache[cache_id] = similarity

                # 若相似度达到阈值，加入到相似组
                if similarity >= threshold:
                    similar_group.similar_videos[test_video.id] = similarity
                    processed_video_id_set.add(test_video.id)

            if len(similar_group.similar_videos) > 0:
                similar_group_list.append(similar_group)

        # 2.精化相似组，处理被重复添加的视频，只保留相似度最大的组
        # TODO

        return similar_group_list
