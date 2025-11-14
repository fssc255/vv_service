import numpy as np


class IVectorDbAccessor:
    def get(self, video_id: str) -> list[np.ndarray] | None:
        """
        根据视频ID获取对应的特征向量

        Args:
            video_id: 视频唯一标识符

        Returns:
            视频对应的特征向量，如果不存在则返回None
        """
        raise NotImplementedError

    def add(self, video_id: str, vectors: list[np.ndarray]) -> None:
        """
        为指定视频ID添加特征向量

        Args:
            video_id: 视频唯一标识符
            vector: 要存储的特征向量
        """
        raise NotImplementedError

    def delete(self, video_id: str) -> None:
        """
        根据视频ID删除对应的特征向量

        Args:
            video_id: 视频唯一标识符
        """
        raise NotImplementedError
