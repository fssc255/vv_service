from models.tables.Video import Video
from models.VideoMetadata import VideoMetadata


class IDbAccessor:
    def get_videos(self) -> list[Video]:
        raise NotImplementedError
