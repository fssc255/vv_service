from Config import Config
from dataclasses import dataclass
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from typing import Any
import mysql.connector


@dataclass
class Video:
    id: str
    video_url: str
    cover_url: str
    size: str
    name: str
    uploader: str
    content: str
    record_time: str
    upload_time: str


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
                    id=row['id'],
                    video_url=row['video_url'],
                    cover_url=row['cover_url'],
                    size=row['size'],
                    name=row['name'],
                    uploader=row['uploader'],
                    content=row['content'],
                    record_time=row['record_time'],
                    upload_time=row['upload_time']
                )
                videos.append(video)

            return videos
        except mysql.connector.Error as e:
            print(f"数据库查询错误: {e}")
            return []
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
