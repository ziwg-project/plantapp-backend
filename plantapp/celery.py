import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantapp.settings')
app = Celery("tasks")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def send_notification(user_pk, title, body):
    from fcm_django.models import FCMDevice
    user_devices = FCMDevice.objects.filter(user_id=user_pk)
    user_devices.send_message(title=title, body=body, sound=True)
