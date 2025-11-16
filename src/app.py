from fastapi import FastAPI, Query, File, UploadFile
from typing import Union, List
from models.requests.VideoAddRequest import VideoAddRequest
from models.responses.ApiResponse import ApiResponse
from models.responses.SimilarVideosResponse import SimilarVideosResponse
from models.responses.VideoAddResponse import VideoAddResponse
from models.responses.VideoRemoveResponse import VideoRemoveResponse
from VAService import VAService
from Config import Config
from utils.Logger import Logger
from PIL import Image
import uvicorn
import io
import base64

app = FastAPI()
va_service = VAService()


def unhandled_error(e: Exception):
    Logger.error(f"{e}")
    return ApiResponse(
        success=False,
        message=f"Unhandled Error: {type(e)}{e}",
    )


@app.get("/")
async def hello_world():
    return "hello world"


@app.post("/api/va/videos", response_model=Union[VideoAddResponse, ApiResponse])
async def add_video(body: VideoAddRequest):
    Logger.info(f"添加视频 (VideoId={body.video_id}, File={body.video_file_path})")
    try:
        video_metadata = va_service.add_video(body.video_id, body.video_file_path)
        if video_metadata is None:
            raise Exception("无法获取视频元数据")

        return VideoAddResponse(
            success=True,
            message="",
            data=video_metadata
        )
    except Exception as e:
        return unhandled_error(e)


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


@app.delete("/api/va/videos/{video_id}", response_model=Union[VideoRemoveResponse, ApiResponse])
async def delete_video(video_id: str):
    try:
        Logger.info(f"删除视频 (VideoId={video_id})")
        deleted = va_service.delete_video(video_id)

        return VideoRemoveResponse(
            success=deleted,
            message=""
        )
    except Exception as e:
        return unhandled_error(e)


# 为Go后端提供的embedding接口
@app.post("/embed")
async def embed_image(file: UploadFile = File(...)):
    """Single image embedding"""
    try:
        # 读取上传的图片
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # 转换为RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 提取特征向量
        import numpy as np
        image_array = np.array(image)
        embedding = va_service.extract_image_embedding(image_array)
        
        return {"vector": embedding, "dimension": len(embedding)}
    except Exception as e:
        Logger.error(f"提取图像特征失败: {e}")
        return {"error": str(e)}


@app.post("/embed_batch")
async def embed_images_batch(files: List[UploadFile] = File(...)):
    """Batch image embedding"""
    try:
        embeddings = []
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            import numpy as np
            image_array = np.array(image)
            embedding = va_service.extract_image_embedding(image_array)
            embeddings.append(embedding)
        
        return {"vectors": embeddings, "count": len(embeddings)}
    except Exception as e:
        Logger.error(f"批量提取图像特征失败: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6590)
