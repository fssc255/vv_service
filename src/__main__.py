from my_va.MyVideoAnalyzer import MyVideoAnalyzer


def test():
    from VideoMetadataExtractor import VideoMetadataExtractor

    print(VideoMetadataExtractor().get_metadata(
        R"/mnt/c/Users/11717/Desktop/old_files/视频类/(.mp4) MP4 视频文件/00087.mp4"
    ))

import utils.DbAccessor_example
import utils.KeyframesSampler_example
import utils.Logger_example

# utils.DbAccessor_example.example()
# utils.KeyframesSampler_example.example()
utils.Logger_example.example()

# va = MyVideoAnalyzer()

# print(va.get_similarity("a", "b"))
# print(va.add_video("a", ""))
