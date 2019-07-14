from __future__ import absolute_import
from celery import shared_task, task
from . import models
import logging
import datetime
import os

logger = logging.getLogger('UI.tasks')


@shared_task
def clear_uploaded_images():
    expired_models = models.UploadedImages.objects.filter(date__lt=datetime.datetime.now()-datetime.timedelta(minutes=10))
    for model in expired_models:
        image = model.image
        try:
            os.remove('static/uploaded_images/' + image)
        except FileNotFoundError as ex:
            logger.warning('Couldn\'t remove static/uploaded_images/' + image)
    expired_models.delete()
