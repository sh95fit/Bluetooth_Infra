# from celery import Celery
import mysql.connector
import os
import logging
from dotenv import load_dotenv
# from config import celeryconfig

from tasks.module import app

load_dotenv()

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


# app = Celery('save_to_mysql', broker=os.getenv('CELERY_BROKER_URL'))
# app.config_from_object('config.celeryconfig')
# app.config_from_object(celeryconfig)

logger.info(f"Celery app configured: {app}")


@app.task()
def save_data_to_db(data):
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=os.getenv('MYSQL_PORT'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv("MYSQL_DB")
        )

        cursor = connection.cursor()

        cursor.execute("INSERT INTO testdata (addr, message) VALUES (%s, %s)",
                       (data['address'], data['message']))

        connection.commit()

        logger.info(
            f"Successfully inserted data into MySQL: addr={data['address']}, message={data['message']}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        logger.error(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("MySQL connection closed")
