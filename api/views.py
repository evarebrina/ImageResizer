from django.http import JsonResponse
from celery.result import AsyncResult
from . import exceptions
import requests
from api.tasks import handle_image
from . import models
import uuid
import logging

logger = logging.getLogger('api.view')


def resize(request):
    try:
        image_url = request.GET.get('image_url', '')
        raw_height = request.GET.get('height', '')
        raw_width = request.GET.get('width', '')
        logger.debug('New request: %s %s %s' % (image_url, raw_height, raw_width))
        # validate height and width
        if image_url == '':
            raise exceptions.NoRequiredParameter('no_url', 'Url not specified')
        if raw_height == '':
            raise exceptions.NoRequiredParameter('no_height', 'Height not specified')
        if raw_width == '':
            raise exceptions.NoRequiredParameter('no_width', 'Width not specified')
        try:
            height = int(raw_height)
        except ValueError:
            raise exceptions.NotAnInteger('wrong_height', 'Height is not an integer')
        try:
            width = int(raw_width)
        except ValueError:
            raise exceptions.NotAnInteger('wrong_width', 'Width is not an integer')
        if height < 1 or height > 9999:
            raise exceptions.OutOfBounds('wrong_height', 'Height is less than 1 or greater than 9999')
        if width < 1 or width > 9999:
            raise exceptions.OutOfBounds('wrong_width', 'Width is less than 1 or greater than 9999')
        # open url ====================================== #
        try:
            image_request = requests.get(image_url)
        except requests.exceptions.MissingSchema:
            raise exceptions.InvalidUrl('wrong_url', 'Image url is invalid')
        # check image =================================== #
        if image_request.status_code != requests.codes.ok:
            raise exceptions.InvalidUrlResponse('response_not_ok', 'Image url error - status code is ' +
                                                str(image_request.status_code) + ', must be 200')
        if image_request.headers['content-type'] == 'image/jpeg':
            extension = '.jpg'
        elif image_request.headers['content-type'] == 'image/png':
            extension = '.png'
        else:
            raise exceptions.InvalidContentType('wrong_content_type', 'wrong content type, must be image/jpeg or \
image/png, not ' + image_request.headers['content-type'])
        if int(image_request.headers['content-length']) > 300000000:
            logger.warning('Content-type is too big %s! It may be not an image' % image_request.headers['content-length'])
        # validation passed ================================== #
        resize_id = str(uuid.uuid4())
        image_name = 'original_' + resize_id + extension
        image_path = 'static/original_images/' + image_name
        logger.debug('Saving file to %s' % image_path)
        f = open(image_path, 'wb+')
        for chunk in image_request.iter_content(1024 * 8):
            if not chunk:
                break
            f.write(chunk)
        f.close()
        logger.debug('Creating model image_path: %s width: %s height: %s' % (image_path, str(width), str(height)))
        model = models.Task(uuid=resize_id, extension=extension)
        logger.debug('Running Task...')
        task = handle_image.delay(resize_id, image_path, extension, height, width)
        logger.debug('Task %s ran' % str(task.id))
        model.task_id = task.id
        model.save()
        logger.debug('Model saved')

    except exceptions.NoRequiredParameter as ex:
        return JsonResponse({
            'status': 'error',
            'error_code': ex.code,
            'message': ex.message,
        }, status=400)
    except exceptions.NotAnInteger as ex:
        return JsonResponse({
            'status': 'error',
            'error_code': ex.code,
            'message': ex.message,
        }, status=400)
    except exceptions.OutOfBounds as ex:
        return JsonResponse({
            'status': 'error',
            'error_code': ex.code,
            'message': ex.message,
        }, status=400)
    except exceptions.InvalidUrl as ex:
        return JsonResponse({
            'status': 'error',
            'error_code': ex.code,
            'message': ex.message,
        }, status=400)
    except exceptions.InvalidUrlResponse as ex:
        return JsonResponse({
            'status': 'error',
            'error_code': ex.code,
            'message': ex.message,
        }, status=400)
    except exceptions.InvalidContentType as ex:
        return JsonResponse({
            'status': 'error',
            'error_code': ex.code,
            'message': ex.message,
        }, status=400)
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({
            'status': 'error',
            'error_code': 'unknown_error',
            'message': 'Unexpected error occurred, please try again',
        }, status=500)
    return JsonResponse({
        'status': 'ok',
        'details': resize_id,
    }, status=201)


def details(request, resize_id):
    try:
        logger.debug('Details requested')
        # may raise exception!!!!!!!!!!!!!!!!!!!!!!!!!!
        model = models.Task.objects.all().get(uuid=resize_id)
        task_id = model.task_id
        task_res = AsyncResult(task_id)
        response = {'status': 'pending'}
        logger.info(task_res.state)
        if task_res.successful():
            image_name = 'sized_' + model.uuid + model.extension
            image_path = '/static/sized_images/' + image_name
            response = {
                'status': 'successful',
                'url': request.get_host() + image_path,
            }
        if task_res.failed():
            logger.warning('task failed')
            response = {
                'status': 'failed',
                'error_code': 'task_failed',
                'message': str(task_res.result),
            }
    except models.Task.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'error_code': 'not_found',
            'message': 'Task not found',
        }, status=404)
    except Exception as ex:
        return JsonResponse({
            'status': 'error',
            'error_code': 'unknown_error',
            'message': 'Unexpected exception occurred',
        }, status=500)
    return JsonResponse(response, status=200)
