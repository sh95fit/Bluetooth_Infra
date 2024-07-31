import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
from tasks.module import app

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME')

# 로그 디렉토리 생성 (디렉토리가 없으면 생성)
os.makedirs('/var/log/celerybeat', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/celerybeat/celery_beat.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@app.task
def delete_7days_ago_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION_NAME]

        seven_days_ago = datetime.now() - timedelta(days=7)

        result = collection.delete_many(
            {"send_time": {"$lt": seven_days_ago.strftime('%Y-%m-%d %H:%M:%S')}})

        client.close()
        logger.info(
            f"Deleted {result.deleted_count} records older than 7 days")

        return f"Deleted {result.deleted_count} records older than 7 days"
    except Exception as e:
        logger.error(f"Error in delete_7days_ago_mongodb : {e}")
        raise
