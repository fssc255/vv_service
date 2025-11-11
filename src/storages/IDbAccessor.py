from models.Video import Video
from models.VideoMetadata import VideoMetadata


class IDbAccessor:
    def get_videos(self) -> list[Video]:
        raise NotImplementedError

    def get_video_metadata(self, video_id: str) -> VideoMetadata | None:
        raise NotImplementedError