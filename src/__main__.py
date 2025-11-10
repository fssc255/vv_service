from my_va.MyVideoAnalyzer import MyVideoAnalyzer


def test():
    from utils.KeyframeSampler import KeyframeSampler

    images = KeyframeSampler.sample(
        video_path=R"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/00016.mp4",
        keyframe_count=10
    )

    for index, image in enumerate(images):
        image.save(fR"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/kf_samples/frame_{index}.jpg")

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
