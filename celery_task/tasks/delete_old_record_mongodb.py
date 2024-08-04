import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
from tasks.module import app
import json

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

        # Mongodb에 message가 JSON 문자열로 저장되어 날짜로 인식 못하는 부분을 조치하기 위한 변환 단계 추가
        # 추후 데이터를 받을 때 애초에 변환을 거치도록 수정 필요
        def convert_message_field():
            for document in collection.find():
                if isinstance(document['message'], str):
                    try:
                        message_dict = json.loads(document['message'])
                        if 'send_time' in message_dict:
                            message_dict['send_time'] = datetime.strptime(
                                message_dict['send_time'], '%Y-%m-%d %H:%M:%S'
                            )
                        collection.update_one(
                            {'_id': document['_id']},
                            {'$set': {'message': message_dict}}
                        )
                    except (json.JSONDecodeError, ValueError) as e:
                        logger.error(
                            f"Error decoding JSON or parsing date: {e}")
                        continue

        convert_message_field()

        seven_days_ago = datetime.now() - timedelta(days=7)
        # test_days_ago = datetime.now() - timedelta(days=1)

        result = collection.delete_many(
            {"message.send_time": {"$lt": seven_days_ago}})
        # result = collection.delete_many(
        #     {"message.send_time": {"$lt": test_days_ago}})

        client.close()

        logger.info(
            f"Deleted {result.deleted_count} records older than 7 days")

        return f"Deleted {result.deleted_count} records older than 7 days"
    except Exception as e:
        logger.error(f"Error in delete_7days_ago_mongodb : {e}")
        raise
