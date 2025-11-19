import os
from VideoSimilarityAnalyzer import VideoSimilarityAnalyzer
from models.SimilarVideoGroup import SimilarVideoGroup
from storages.IDbAccessor import IDbAccessor
from storages.IVectorDbAccessor import IVectorDbAccessor
from utils.Logger import Logger


class VAService:
    def __init__(self, db_accessor: IDbAccessor, vector_db_accessor: IVectorDbAccessor) -> None:
        self.__db_accessor: IDbAccessor = db_accessor
        self.__vector_db_accessor: IVectorDbAccessor = vector_db_accessor

    def find_similar_videos(self, threshold: float) -> list[SimilarVideoGroup]:
        video_similarity_analyzer = VideoSimilarityAnalyzer()

        compare_cache: dict[str, float] = {}
        processed_video_id_set: set[str] = set()
        similar_group_list: list[SimilarVideoGroup] = []

        videos = [x for x in self.__db_accessor.get_videos()
                  if os.path.exists(x.file_path) and (not os.path.isdir(x.file_path))]

        Logger.info(f"正在从{len(videos)}个视频中查找相似视频...")

        # 1.初步筛选相似组
        for order, reference_video in enumerate(videos):
            Logger.info(f"[{order + 1}/{len(videos)}] 当前参考视频: {reference_video.id}")

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

                Logger.info(f"比较 ({reference_video.id}, {test_video.id})")

                if reference_video.id < test_video.id:
                    first_video, second_video = reference_video, test_video
                else:
                    first_video, second_video = test_video, reference_video

                # 先尝试从缓存中获取，没有再调用分析器
                cache_id = f"{first_video.id}:{second_video.id}"
                if cache_id in compare_cache:
                    similarity = compare_cache[cache_id]
                else:
                    similarity = video_similarity_analyzer.get_similarity(first_video, second_video)
                    compare_cache[cache_id] = similarity

                # 若相似度达到阈值，加入到相似组
                if similarity >= threshold:
                    similar_group.similar_videos[test_video.id] = similarity
                    processed_video_id_set.add(test_video.id)

            if len(similar_group.similar_videos) > 0:
                similar_group_list.append(similar_group)

        # 2.精化相似组，处理被重复添加的视频，只保留相似度最大的组
        # 没啥必要了，留着仅做优化提示

        return similar_group_list
