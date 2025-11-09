from dataclasses import dataclass


@dataclass
class VideoMetadata:
    width: int | None
    height: int | None
    fps: float | None
    duration: int | None
    file_type: str
    file_size: int
    create_time: int
    modify_time: int
    md5: str

    def to_dict(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "duration": self.duration,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "create_time": self.create_time,
            "modify_time": self.modify_time,
            "md5": self.md5,
        }
