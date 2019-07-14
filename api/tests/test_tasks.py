from django.test import TestCase
import uuid
import os
from PIL import Image
import datetime
from api.tasks import handle_image, clear_database
from api import models
import logging
logger = logging.getLogger('api.tests.test_tasks')


class HandleImage(TestCase):

    def setUp(self):
        self.resize_id = str(uuid.uuid4())
        self.extension = '.jpg'
        image_name = 'test_image' + self.extension
        self.test_path = 'static/test_images3847/'
        self.test_original_image_path = self.test_path + image_name
        self.test_sized_image_path = 'static/sized_images/' + 'sized_' + self.resize_id + self.extension
        try:
            os.mkdir(self.test_path)
        except FileExistsError:
            logger.error(self.test_path + ' already exists')

    def tearDown(self):
        os.remove(self.test_original_image_path)
        os.rmdir(self.test_path)
        if os.path.exists(self.test_sized_image_path):
            os.remove(self.test_sized_image_path)

    def test_good(self):
        img = Image.new('RGB', (400, 300), color=5)
        img.save(self.test_original_image_path)
        res = handle_image(self.resize_id, self.test_original_image_path, self.extension, 100, 100)
        self.assertEqual(res, 'succeed')

    def test_file_is_not_a_valid_image(self):
        invalid_image = open(self.test_original_image_path, 'w+')
        invalid_image.write('some stuff')
        invalid_image.close()
        with self.assertRaisesMessage(Exception, 'File is not a valid image'):
            handle_image(self.resize_id, self.test_original_image_path, self.extension, 100, 100)


class ClearDatabase(TestCase):

    def setUp(self):
        self.resize_id = str(uuid.uuid4())
        self.extension = '.jpg'
        image_name = self.resize_id + self.extension
        self.original_path = 'static/original_images/'
        self.sized_path = 'static/sized_images/'
        self.original_image_path = self.original_path + 'original_' + image_name
        self.sized_image_path = self.sized_path + 'sized_' + image_name
        f = open(self.original_image_path, 'w+')
        f.close()
        f = open(self.sized_image_path, 'w+')
        f.close()
        date = datetime.datetime.now() - datetime.timedelta(minutes=15)
        model = models.Task(uuid=self.resize_id, extension=self.extension)
        model.save()
        model.date = date
        model.save()

    def tearDown(self):
        if os.path.exists(self.original_image_path):
            os.remove(self.original_image_path)
        if os.path.exists(self.sized_image_path):
            os.remove(self.sized_image_path)

    def test_good(self):
        clear_database()

        self.assertFalse(models.Task.objects.filter(uuid=self.resize_id).exists())
        self.assertFalse(os.path.exists(self.original_image_path))
        self.assertFalse(os.path.exists(self.sized_image_path))
