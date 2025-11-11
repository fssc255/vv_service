from storages.IVectorDbAccessor import IVectorDbAccessor
import numpy as np


class VectorDbAccessor(IVectorDbAccessor):
    def __init__(self, db_file_path: str) -> None:
        self.__db_file_path = db_file_path

    def open(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def get(self, video_id: str) -> list[np.ndarray] | None:
        raise NotImplementedError

    def add(self, video_id: str, vector: list[np.ndarray]) -> None:
        raise NotImplementedError

    def delete(self, video_id: str) -> None:
        raise NotImplementedError
