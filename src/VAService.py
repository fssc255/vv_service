from dataclasses import dataclass
from VideoSimilarityAnalyzer import VideoSimilarityAnalyzer
from models.VideoMetadata import VideoMetadata
from storages.DbAccessor import DbAccessor
from models.Video import Video
from models.SimilarVideoGroup import SimilarVideoGroup
from storages.IDbAccessor import IDbAccessor


class VAService:
    def __init__(self) -> None:
        self.__db_accessor: IDbAccessor = None
        self.__videoSimilarityAnalyzer = VideoSimilarityAnalyzer(
            dbAccessor=None,
            vectorDbAccessor=None,
        )

    def add_video(self, video_id: str, video_file_path: str) -> VideoMetadata:
        return VideoMetadata(
            width=1920,
            height=1080,
            fps=30.0,
            duration=120,
            file_type="mp4",
            file_size=10485760,
            create_time=1698765432,
            modify_time=1698765432,
            md5="5d41402abc4b2a76b9719d911017c592",
        )

    def delete_video(self, video_id: str) -> bool:
        return True

    def find_similar_videos(self, threshold: float) -> list[SimilarVideoGroup]:
        return [
            SimilarVideoGroup(
                reference_video="aow05202",
                similar_videos={
                    "0x0fa9ax": 0.92,
                    "ab90s9fa": 0.85,
                    "aof09sa0": 0.95
                }
            ),
            SimilarVideoGroup(
                reference_video="f2fafaow",
                similar_videos={
                    "jfoeia9e": 0.85,
                    "ojfs9909": 0.95
                }
            )
        ]

        return
        videos = self.__db_accessor.get_videos()

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
                    similarity = self.__videoSimilarityAnalyzer.get_similarity(first_video.id, second_video.id)
                    compare_cache[cache_id] = similarity

                # 若相似度达到阈值，加入到相似组
                if similarity >= threshold:
                    similar_group.similar_videos[test_video.id] = similarity

            if len(similar_group.similar_videos) > 0:
                similar_group_list.append(similar_group)

        # 2.精化相似组，处理被重复添加的视频，只保留相似度最大的组
        # TODO

        return similar_group_list
