# from celery import Celery
import mysql.connector
import os
import logging
from dotenv import load_dotenv

from pymongo import MongoClient

from tasks.module import app

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME')

# 로그 디렉토리 생성 (디렉토리가 없으면 생성)
os.makedirs('/var/log/celerytask', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/celerytask/celery_task.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@app.task()
def save_data_to_mongo(addr, message):
    try:
        # MongoDB 클라이언트 설정
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION_NAME]

        collection.insert_one({
            'address': str(addr),
            'message': message
        })
        logger.info(f"Inserted document: {message}")

    except Exception as e:
        logger.error(f"Error inserting document into MongoDB: {e}")
