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

        # Sample 데이터 (추후 시공사, 발전소 데이터와 연결이 필요한 구간)
        UNTID = "Hun's Company"
        IVTID = "ESP25K_2"
        SERIALNO = "00000000000000000000"
        PHASE = "1"
        CO2_PARAM = 0.46625

        if data['length'] == 120:
            DATA_UNIT = 1000
            cursor.execute("INSERT INTO bledata (UNTID, IVTID, SERIALNO, EVTDATME, PHASE, STATIONNO, ERRCD, INV1, INV2, INV3, INV4, INV5, INV6, INA1, INA2, INA3, INA4, INA5, INA6, OUTVR, OUTVS, OUTVT, OUTAR, OUTAS, OUTAT, TEMP, TPG, RUNTYPE, CPG, INVERRCD, TOTAL_CO2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (UNTID, IVTID, SERIALNO, data['savetime'], PHASE, data['device_id'], data['message'], data['inv1'], data['inv2'], data['inv3'], data['inv4'], data['inv5'], data['inv6'], data['ina1'], data['ina2'], data['ina3'], data['ina4'], data['ina5'], data['ina6'], data['outvrs'], data['outvst'], data['outvtr'], data['outar'], data['outas'], data['outat'], data['temp'], data['tpg'], data['operation'], data['cpg'], data['message'], data['cpg']*CO2_PARAM/DATA_UNIT))
        else:
            logger.error(f"Incorrect Data Length ...")

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
