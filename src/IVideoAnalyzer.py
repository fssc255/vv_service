class IVideoAnalyzer:
    def add_video(self, video_id: str, video_file_path: str) -> None:
        """
        向数据库添加视频

        Args:
            video_id (str): 视频的唯一标识符
            video_file_path (str): 视频的文件路径

        Raises:
            InvalidVideoIdError: 当 video_id 已被添加时抛出
            Error: 其他错误
        """
        pass

    def get_similarity(self, video_id_a: str, video_id_b: str) -> float:
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
        pass
