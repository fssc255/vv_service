from datetime import datetime
from io import TextIOWrapper
from Config import Config
import os


class Logger:
    __fp: TextIOWrapper | None = None

    @staticmethod
    def initialize():
        if Logger.__fp is not None:
            return

        if not os.path.exists(Config.LOG_DIRECTORY):
            os.makedirs(Config.LOG_DIRECTORY)

        current_time = datetime.now().strftime("%Y-%m-%d")
        Logger.__fp = open(os.path.join(Config.LOG_DIRECTORY, f"log_{current_time}.txt"), mode="a", encoding="utf8")

    @staticmethod
    def close():
        if Logger.__fp is not None:
            Logger.__fp.close()

    @staticmethod
    def info(message: str) -> None:
        Logger.__write_log_message(message, "Info")

    @staticmethod
    def debug(message: str) -> None:
        Logger.__write_log_message(message, "Debug")

    @staticmethod
    def warning(message: str) -> None:
        Logger.__write_log_message(message, "Warning")

    @staticmethod
    def error(message: str) -> None:
        Logger.__write_log_message(message, "Error")

    @staticmethod
    def __write_log_message(log_message: str, category) -> None:
        if Logger.__fp is None:
            Logger.initialize()

        assert Logger.__fp is not None

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Logger.__fp.write(f"[{current_time}] [{category}] {log_message}\n")
        print(log_message)
