from django.test import TestCase, RequestFactory
from .views import rest_resize
import json


class RestResize(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_good(self):
        request = self.factory.get('/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&height=100&width=100', HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 201)

    def test_empty_url(self):
        request = self.factory.get(
            '/?height=100&width=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'no_url',
            'message': 'Url not specified',
        })

    def test_empty_height(self):
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&width=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'no_height',
            'message': 'Height not specified',
        })

    def test_empty_height(self):
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&height=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'no_width',
            'message': 'Width not specified',
        })

    def test_height_is_not_an_int(self):
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&width=100&height=ggg',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_height',
            'message': 'Height is not an integer',
        })

    def test_width_is_not_an_int(self):
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&width=ggg&height=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_width',
            'message': 'Width is not an integer',
        })

    def test_width_is_out_of_bounds(self):
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&width=10000&height=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_width',
            'message': 'Width is less than 1 or greater than 9999',
        })
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&width=0&height=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_width',
            'message': 'Width is less than 1 or greater than 9999',
        })

    def test_height_is_out_of_bounds(self):
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&width=100&height=10000',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_height',
            'message': 'Height is less than 1 or greater than 9999',
        })
        request = self.factory.get(
            '/?image_url=http://31.134.134.147:8000/static/sized_images/sized_dd01ce84-2eba-428d-8593-088eb0cf3774.jpg&width=100&height=0',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_height',
            'message': 'Height is less than 1 or greater than 9999',
        })

    def test_invalid_url(self):
        request = self.factory.get(
            '/?image_url=invalidurl&width=100&height=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_url',
            'message': 'Image url is invalid',
        })

    def test_url_not_ok(self):
        request = self.factory.get(
            '/?image_url=http://example.com/photo.jpg&width=100&height=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'response_not_ok',
            'message': 'Image url error - status code is 404, must be 200',
        })

    def test_url_is_not_image(self):
        request = self.factory.get(
            '/?image_url=https://stackoverflow.com/questions/4283933/what-is-the-clean-way-to-unittest-filefield-in-django&width=100&height=100',
            HTTP_HOST='31.134.134.147:8000')
        response = rest_resize(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'status': 'error',
            'error_code': 'wrong_content_type',
            'message': 'wrong content type, must be image/jpeg or image/png, not text/html; charset=utf-8',
        })
