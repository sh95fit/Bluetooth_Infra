import os
from dotenv import load_dotenv
from celery import Celery
from config import celeryconfig

load_dotenv()

app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'))
app.config_from_object(celeryconfig)
