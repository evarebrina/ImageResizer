from django.db import models

# original image name: original_ + uuid + extension
# sized image name: sized_ + uuid + extension


class Task(models.Model):
    uuid = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=150, null=True)
    extension = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return self.uuid
