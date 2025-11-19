from Config import Config
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from typing import Any
from models.tables.Video import Video
from storages.IDbAccessor import IDbAccessor
from utils.Logger import Logger
import mysql.connector


class DbAccessor(IDbAccessor):
    def __init__(self) -> None:
        self.__conn: PooledMySQLConnection | MySQLConnectionAbstract | None = None

    def open(self) -> None:
        self.__conn = mysql.connector.connect(
            host=Config.Database.HOST,
            port=Config.Database.PORT,
            user=Config.Database.USER,
            password=Config.Database.PASSWORD,
            database=Config.Database.DB_NAME,
        )

        if not self.__conn.is_connected():
            raise ConnectionError("数据库连接失败")

    def close(self) -> None:
        if self.__conn is not None and self.__conn.is_connected():
            self.__conn.close()

    def get_videos(self) -> list[Video]:
        if self.__conn is None:
            raise Exception("Database is not open")

        query = """
        SELECT id, file_path
        FROM videos
        """

        cursor = self.__conn.cursor(dictionary=True)

        try:
            cursor.execute(query)
            results: Any = cursor.fetchall()

            videos = []
            for row in results:
                video = Video(
                    id=row["id"],
                    file_path=row["file_path"],
                )
                videos.append(video)

            return videos
        except Exception as e:
            Logger.error(f"查询数据库时出现错误: SQL={query}, Error={e}")
            return []
        finally:
            cursor.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
