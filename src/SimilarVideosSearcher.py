from dataclasses import dataclass
from VideoAnalyzer import VideoAnalyzer
from storages.DbAccessor import DbAccessor
from models.Video import Video
from models.SimilarVideoGroup import SimilarVideoGroup


class SimilarVideosSearcher:
    @staticmethod
    def find_similar_videos(videoAnalyzer: VideoAnalyzer, threshold: float) -> list[SimilarVideoGroup]:
        with DbAccessor() as db_accessor:
            videos = db_accessor.get_videos()

        compare_cache: dict[str, float] = {}
        similar_group_list: list[SimilarVideoGroup] = []

        # 1.筛选相似组
        for reference_video in videos:
            similar_group = SimilarVideoGroup(
                reference_video=reference_video.id,
                similar_videos={}
            )
            for test_video in videos:
                # 跳过自比较
                if reference_video.id == test_video.id:
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
                    similarity = videoAnalyzer.get_similarity(first_video.id, second_video.id)
                    compare_cache[cache_id] = similarity

                # 若相似度达到阈值，加入到相似组
                if similarity >= threshold:
                    similar_group.similar_videos[test_video.id] = similarity

            if len(similar_group.similar_videos) > 0:
                similar_group_list.append(similar_group)

        # 2.精化相似组，处理被重复添加的视频，只保留相似度最大的组
        # TODO

        return []
