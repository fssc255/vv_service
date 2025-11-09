from IVideoAnalyzer import IVideoAnalyzer
from errors.InvalidVideoIdError import InvalidVideoIdError
import random


class MyVideoAnalyzer(IVideoAnalyzer):
    def add_video(self, video_id: str, video_file_path: str) -> None:
        raise InvalidVideoIdError
        pass

    def get_similarity(self, video_id_a: str, video_id_b: str) -> float:
        return random.random()
