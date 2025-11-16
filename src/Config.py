class Config:
    class Database:
        HOST = "127.0.0.1"
        PORT = 3306
        USER = "root"
        PASSWORD = "XXXX"  
        DB_NAME = "video_manage_system"

    class VectorDatabase:
        DB_PATH = "./vector_db"  

    API_BASE_URL = "127.0.0.1"
    PORT = 6590
    VIDEO_LIBRARY = "./video_library"
    LOG_DIRECTORY = "./logs"
    DEFAULT_SIMILARITY_THRESHOLD = 0.95
