import os


class Config:
    class Database:
        HOST = os.getenv("VMS_VA_DATABASE_HOST", "127.0.0.1")
        PORT = int(os.getenv("VMS_VA_DATABASE_PORT", "3306"))
        USER = os.getenv("VMS_VA_DATABASE_USER", "root")
        PASSWORD = os.getenv("VMS_VA_DATABASE_PASSWORD", "123456")
        DB_NAME = os.getenv("VMS_VA_DATABASE_NAME", "video_manage_system")

    class VectorDatabase:
        DB_PATH = os.getenv("VMS_VA_VECTOR_DATABASE_PATH", "./vector_db")

    API_BASE_URL = os.getenv("VMS_VA_API_BASE_URL", "0.0.0.0")
    PORT = int(os.getenv("VMS_VA_API_PORT", "6590"))
    LOG_DIRECTORY = os.getenv("VMS_VA_LOG_DIR", "./logs")
    DEFAULT_SIMILARITY_THRESHOLD = float(os.getenv("VMS_VA_DEFAULT_SIMILARITY_THRESHOLD", "0.95"))
    RESNET18_WEIGHTS_PATH = os.getenv("VMS_VA_RESNET18_WEIGHTS_PATH", "./weights/resnet18-f37072fd.pth")
