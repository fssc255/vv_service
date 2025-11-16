from storages.IVectorDbAccessor import IVectorDbAccessor
from Config import Config
from utils.Logger import Logger
import numpy as np
import chromadb
from chromadb.config import Settings


class VectorDbAccessor(IVectorDbAccessor):
    """ChromaDB向量数据库访问器"""
    
    def __init__(self, collection_name: str = "video_embeddings") -> None:
        try:
            # 初始化ChromaDB客户端
            self.__client = chromadb.PersistentClient(
                path=Config.VectorDatabase.DB_PATH,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # 获取或创建集合
            try:
                self.__collection = self.__client.get_collection(name=collection_name)
                Logger.info(f"使用已存在的ChromaDB集合: {collection_name}")
            except:
                self.__collection = self.__client.create_collection(
                    name=collection_name,
                    metadata={"description": "视频特征向量存储"}
                )
                Logger.info(f"创建新的ChromaDB集合: {collection_name}")
                
        except Exception as e:
            Logger.error(f"初始化ChromaDB失败: {e}")
            raise

    def get(self, video_id: str) -> list[np.ndarray] | None:
        """获取视频的特征向量列表"""
        try:
            results = self.__collection.get(
                ids=[video_id],
                include=["embeddings", "metadatas"]
            )
            
            if not results["ids"] or not results["embeddings"]:
                return None
            
            # ChromaDB返回的是二维列表
            embeddings = results["embeddings"][0]
            
            # 获取帧数信息
            frame_count = 1
            if results["metadatas"] and len(results["metadatas"]) > 0:
                metadata = results["metadatas"][0]
                if metadata and "frame_count" in metadata:
                    fc = metadata["frame_count"]
                    if isinstance(fc, (int, float)):
                        frame_count = int(fc)
            
            if frame_count > 1:
                # 将扁平化的向量重构为多个帧向量
                vector_dim = len(embeddings) // frame_count
                vectors = [
                    np.array(embeddings[i*vector_dim:(i+1)*vector_dim], dtype=np.float32)
                    for i in range(frame_count)
                ]
                return vectors
            else:
                return [np.array(embeddings, dtype=np.float32)]
                
        except Exception as e:
            Logger.error(f"从ChromaDB获取向量失败 (VideoId={video_id}): {e}")
            return None

    def add(self, video_id: str, vectors: list[np.ndarray]) -> None:
        """添加视频的特征向量列表"""
        try:
            # 将多个帧向量扁平化为单个向量存储
            # ChromaDB每个ID只能存储一个向量，我们将多帧向量拼接
            flattened_vector = np.concatenate(vectors).tolist()
            
            # 准备元数据
            metadata = {
                "frame_count": len(vectors),
                "vector_dim": len(vectors[0]) if len(vectors) > 0 else 0
            }
            
            # 添加到ChromaDB
            self.__collection.upsert(
                ids=[video_id],
                embeddings=[flattened_vector],
                metadatas=[metadata]
            )
            
            Logger.info(f"成功添加向量到ChromaDB (VideoId={video_id}, Frames={len(vectors)})")
            
        except Exception as e:
            Logger.error(f"添加向量到ChromaDB失败 (VideoId={video_id}): {e}")
            raise

    def delete(self, video_id: str) -> None:
        """删除视频的特征向量"""
        try:
            self.__collection.delete(ids=[video_id])
            Logger.info(f"从ChromaDB删除向量成功 (VideoId={video_id})")
        except Exception as e:
            Logger.error(f"从ChromaDB删除向量失败 (VideoId={video_id}): {e}")
            raise
