from Config import Config
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from typing import Any
from models.Video import Video
from models.VideoMetadata import VideoMetadata
from utils.Logger import Logger
import mysql.connector


class DbAccessor:
    def __init__(self) -> None:
        self.__conn:  MySQLConnectionAbstract | PooledMySQLConnection | None = None

    def get_videos(self) -> list[Video]:
        query = """
        SELECT id, video_url, cover_url, size, name, uploader, content, record_time, upload_time
        FROM videos
        ORDER BY upload_time DESC
        """

        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query)
            results: Any = cursor.fetchall()

            videos = []
            for row in results:
                video = Video(
                    id=row["id"],
                    video_url=row["video_url"],
                    cover_url=row["cover_url"],
                    size=row["size"],
                    name=row["name"],
                    uploader=row["uploader"],
                    content=row["content"],
                    record_time=row["record_time"],
                    upload_time=row["upload_time"]
                )
                videos.append(video)

            return videos
        except Exception as e:
            Logger.error(f"查询数据库时出现错误: SQL={query}, Error={e}")
            return []
        finally:
            cursor.close()

    def get_video_metadata(self, video_id: str) -> VideoMetadata | None:
        query = f"""
        SELECT id, video_id, width, height, fps, duration, file_type, file_size, create_time, modify_time, md5
        FROM video_metadata
        WHERE video_id=%s
        """

        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (video_id,))
            result: Any = cursor.fetchone()

            if result is None:
                return None

            video_metadata = VideoMetadata(
                width=result["width"],
                height=result["height"],
                fps=result["fps"],
                duration=result["duration"],
                file_type=result["file_type"],
                file_size=result["file_size"],
                create_time=result["create_time"],
                modify_time=result["modify_time"],
                md5=result["md5"],
            )
            return video_metadata
        except Exception as e:
            Logger.error(f"查询数据库时出现错误: SQL={query}, Error={e}")
            return None
        finally:
            cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close_connection()

    def __get_connection(self):
        if self.__conn is not None and self.__conn.is_connected():
            return self.__conn

        self.__conn = mysql.connector.connect(
            host=Config.Database.HOST,
            port=Config.Database.PORT,
            user=Config.Database.USER,
            password=Config.Database.PASSWORD,
            database=Config.Database.DB_NAME,
        )

        return self.__conn

    def __close_connection(self):
        if self.__conn is not None and self.__conn.is_connected():
            self.__conn.close()
            self.__conn = None
