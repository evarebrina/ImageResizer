from django.db import models


class Task(models.Model):
    uuid = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=150, null=True)
    original_image = models.CharField(max_length=150)
    sized_image = models.CharField(max_length=150)

    def __str__(self):
        return self.uuid
