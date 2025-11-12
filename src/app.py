from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from models.VARequest import VARequest
from models.VideoMetadata import VideoMetadata
from models.SimilarVideoGroup import SimilarVideoGroup
import uvicorn

class ApiResponse(BaseModel):
    success: bool
    message: str


class SimilarVideosResponse(ApiResponse):
    data: Optional[list[SimilarVideoGroup]] = None


class VideoAddResponse(ApiResponse):
    data: Optional[VideoMetadata] = None


class VideoRemoveResponse(ApiResponse):
    pass

app = FastAPI()

@app.get("/")
async def hello_world():
    return "Hello, World!"


@app.post("/api/va", response_model=Union[ApiResponse, VideoAddResponse, VideoRemoveResponse, SimilarVideosResponse])
async def video_analyzer(request_data: VARequest):
    def add_video():
        video_id = request_data.video_id
        video_file_path = request_data.video_file_path
        print(f"Adding video {video_id} (path={video_file_path})")
        data = VideoMetadata(
            width=1920,
            height=1080,
            fps=30.0,
            duration=120,
            file_type="mp4",
            file_size=10485760,
            create_time=1698765432,
            modify_time=1698765432,
            md5="5d41402abc4b2a76b9719d911017c592",
        )
        return VideoAddResponse(
            success=True,
            message="",
            data=data
        )

    def remove_video():
        video_id = request_data.video_id
        print(f"Removing video {video_id}")
        return VideoRemoveResponse(
            success=True,
            message=""
        )

    def find_similar_videos():
        print("Finding similar videos...")
        data = [
            SimilarVideoGroup(
                reference_video="aow05202",
                similar_videos={
                    "0x0fa9ax": 0.92,
                    "ab90s9fa": 0.85,
                    "aof09sa0": 0.95
                }
            ),
            SimilarVideoGroup(
                reference_video="f2fafaow",
                similar_videos={
                    "jfoeia9e": 0.85,
                    "ojfs9909": 0.95
                }
            )
        ]
        return SimilarVideosResponse(
            success=True,
            message="",
            data=data
        )

    match request_data.action:
        case "VA:FIND_SIMILAR_VIDEOS":
            return find_similar_videos()
        case "VA:ADD_VIDEO":
            return add_video()
        case "VA:REMOVE_VIDEO":
            return remove_video()

    return ApiResponse(
        success=False,
        message="Unknown action request"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6590)
