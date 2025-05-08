import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    CONTEXT_EXPIRY_SECONDS = int(os.getenv("CONTEXT_EXPIRY_SECONDS", 86400))
    CSV_FILE_PATH = os.getenv("CSV_FILE_PATH", "Q&A.csv")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index")

settings = Settings()