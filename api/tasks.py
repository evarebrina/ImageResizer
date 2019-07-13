from __future__ import absolute_import
from celery import shared_task
from PIL import Image
from . import models
import logging
import datetime
import os

logger = logging.getLogger('api.tasks')


@shared_task
def handle_image(resize_id, original_image_path, extension, h, w):
    try:
        logger.info('handler: opening file: ' + original_image_path)
        # may raise an IOError!!!!!!!!!!!!!!!!!!!!!!!!!!
        original_image = Image.open(original_image_path)
        sized_image = original_image.resize((w, h))
        image_name = 'sized_' + resize_id + extension
        logger.info('Processed image ' + image_name)
        image_path = 'static/sized_images/' + image_name
        sized_image.save(image_path, original_image.format)
        # may raise models.Task.DoesNotExist!!!!!!!!!!!!
        model = models.Task.objects.get(uuid=resize_id)
        model.sized_image = image_name
        model.save()
        logger.info('handler: finished')
    except IOError as ex:
        logger.exception(ex)
        raise Exception('File is not a valid image')
    except models.Task.DoesNotExist as ex:
        logger.exception(ex)
        raise Exception('unexpected error: no entry in database')
    return 'succeed'


@shared_task
def clear_database():
    expired_models = models.Task.objects.filter(date__lt=datetime.datetime.now()-datetime.timedelta(minutes=10))
    for model in expired_models:
        original_image = model.original_image
        sized_image = model.sized_image
        try:
            os.remove('static/original_images/' + original_image)
        except FileNotFoundError as ex:
            logger.warning('File ' + original_image + ' does not exist')
        try:
            os.remove('static/sized_images/' + sized_image)
        except FileNotFoundError as ex:
            logger.warning('File ' + sized_image + ' does not exist')
        logger.info('Removed ' + original_image + ' and ' + sized_image)
    expired_models.delete()
    logger.info('Removed database entry')
