from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class VectorsSimilarityCalculator:
    def calculate(self, first_vectors: list[np.ndarray], second_vectors: list[np.ndarray]) -> float:
        """
        计算两个向量的相似度

        Args:
            first_vectors (str): 向量组
            second_vectors (str): 向量组

        Returns:
            float: 相似度得分，范围在[0,1]之间，值越高相似度越高
        """
        if len(first_vectors) != len(second_vectors):
            return 0

        if len(first_vectors) == 0:
            return 0

        frac = 1 / len(first_vectors)

        # 视频1的关键帧匹配视频2的关键帧
        similarity_a = 0
        for vector in first_vectors:
            similarities = cosine_similarity(vector.reshape(1, -1), second_vectors)[0]  # type:ignore
            similarity_a += max(similarities) * frac

        # 视频2的关键帧匹配视频1的关键帧（避免单向匹配偏差）
        similarity_b = 0
        for vector in second_vectors:
            similarities = cosine_similarity(vector.reshape(1, -1), first_vectors)[0]  # type:ignore
            similarity_b += max(similarities) * frac

        return (similarity_a + similarity_b) / 2
