from celery import Celery, Task
from flask import current_app as app

def init_celery():
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery_app = Celery()
    return celery_app

celery = init_celery()
