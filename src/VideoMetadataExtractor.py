from models.VideoMetadata import VideoMetadata
from pymediainfo import MediaInfo
from typing import Any
import os
import hashlib


class VideoMetadataExtractor:
    @staticmethod
    def get_metadata(video_file_path: str) -> VideoMetadata:
        def parse_int(value: Any) -> int | None:
            try:
                return int(value)
            except:
                return None

        def parse_float(value: Any) -> float | None:
            try:
                return float(value)
            except:
                return None

        if not os.path.exists(video_file_path):
            raise FileNotFoundError(video_file_path)

        metadata = {
            "id": -1,
            "video_id": "",
        }
        media_info = MediaInfo.parse(video_file_path)

        file_stat = os.stat(video_file_path)
        metadata |= {
            "file_size": file_stat.st_size,
            "create_time": parse_int(file_stat.st_ctime),
            "modify_time": parse_int(file_stat.st_mtime),
        }

        for track in media_info.tracks:
            track_type = track.track_type.lower()
            if track_type == "general":
                metadata["file_type"] = track.format.lower()
            if track_type == "video":
                duration = parse_float(track.duration)
                metadata |= {
                    "width": parse_int(track.width),
                    "height": parse_int(track.height),
                    "fps": parse_float(track.frame_rate),
                    "duration": int(duration / 1000) if duration is not None else -1,
                }
                break

        metadata["md5"] = VideoMetadataExtractor.__calculate_md5(video_file_path)

        return VideoMetadata(**metadata)

    @staticmethod
    def __calculate_md5(file_path: str, chunk_size: int = 8192) -> str | None:
        try:
            md5_hash = hashlib.md5()

            # 分块读取文件计算MD5
            with open(file_path, "rb") as file:
                chunk = file.read(chunk_size)
                while chunk:
                    md5_hash.update(chunk)
                    chunk = file.read(chunk_size)

            return md5_hash.hexdigest().lower()
        except:
            return None
