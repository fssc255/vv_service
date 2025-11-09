from my_va.MyVideoAnalyzer import MyVideoAnalyzer


def test():
    from DbAccessor import DbAccessor
    from VideoMetadataExtractor import VideoMetadataExtractor

    db_accessor = DbAccessor()
    print(db_accessor.get_videos())

    print(VideoMetadataExtractor().get_metadata(
        R"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/00087.mp4"
    ))


va = MyVideoAnalyzer()

print(va.get_similarity("a", "b"))
print(va.add_video("a", ""))
