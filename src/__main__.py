from my_va.MyVideoAnalyzer import MyVideoAnalyzer


def test():
    def save_images(keyframe_images, dir_name):
        for index, image in enumerate(keyframe_images):
            image.save(fR"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/{dir_name}/frame_{index}.jpg")

    from utils.KeyframeSampler import KeyframeSampler, IKeyframeSelector

    # 1：自动平均间隔采样（恒定数量）
    keyframe_images = KeyframeSampler.sample(
        video_file_path=R"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/00016.mp4",
        keyframe_count=10,
    )
    save_images(keyframe_images, "kf1")


    # 2：自定义采样点
    class WTFKeyframeSelector(IKeyframeSelector):
        def get_frame_position(self, keyframe_index: int, total_frame_count: int) -> int:
            # 第 i 个关键帧在视频的第 i * 90 帧获取
            return keyframe_index * 90

    keyframe_images = KeyframeSampler.sample(
        video_file_path=R"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/00016.mp4",
        keyframe_count=10,
        keyframe_selector=WTFKeyframeSelector()
    )
    save_images(keyframe_images, "kf2")


    # 3：固定时间间隔采样（恒定时间间隔）
    keyframe_images = KeyframeSampler.sample_at_fixed_interval(
        video_file_path=R"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/00016.mp4",
        interval=3
    )
    save_images(keyframe_images, "kf3")

    return
    from DbAccessor import DbAccessor
    from VideoMetadataExtractor import VideoMetadataExtractor

    db_accessor = DbAccessor()
    print(db_accessor.get_videos())

    print(VideoMetadataExtractor().get_metadata(
        R"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/00087.mp4"
    ))


test()
# va = MyVideoAnalyzer()

# print(va.get_similarity("a", "b"))
# print(va.add_video("a", ""))
