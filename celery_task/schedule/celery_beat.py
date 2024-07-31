from celery.schedules import crontab
from tasks.module import app

app.conf.timezone = 'Asia/Seoul'
app.conf.beat_schedule = {
    'delete-old-documents-daily': {
        'task': 'tasks.delete_old_record_mongodb.delete_7days_ago_mongodb',
        'schedule': crontab(hour=23, minute=0),  # 매일 밤 11시
        # 'schedule': crontab(minute="*"),  # 적용 테스트
    },
}
