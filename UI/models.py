from django.db import models


class UploadedImages(models.Model):
    image = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
