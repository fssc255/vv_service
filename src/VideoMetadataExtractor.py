from models.VideoMetadata import VideoMetadata


class VideoMetadataExtractor:
    def get_metadata(self, video_file_path) -> VideoMetadata:
        metadata = {}

        return VideoMetadata(
            **metadata
        )
