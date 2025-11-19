from fastapi import FastAPI, Query
from typing import Union
from models.responses.ApiResponse import ApiResponse
from models.responses.SimilarVideosResponse import SimilarVideosResponse
from VAService import VAService
from Config import Config
from utils.Logger import Logger
import uvicorn


def unhandled_error(e: Exception):
    Logger.error(f"{e}")
    return ApiResponse(
        success=False,
        message=f"Unhandled Error: {type(e)}{e}",
    )


va_service = VAService()
app = FastAPI()


@app.get("/")
async def hello_world():
    return "hello world"


@app.get("/api/va/similar-videos", response_model=Union[SimilarVideosResponse, ApiResponse])
async def similar_videos(
    threshold: float = Query(default=Config.DEFAULT_SIMILARITY_THRESHOLD, ge=0.0, le=1.0)
):
    try:
        Logger.info(f"查找相似视频中 (threshold={threshold})")
        similar_videos = va_service.find_similar_videos(threshold)

        return SimilarVideosResponse(
            success=True,
            message="",
            data=similar_videos
        )
    except Exception as e:
        return unhandled_error(e)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6590)
