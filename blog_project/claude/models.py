from django.db import models

class DataEntry(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    chat_messages = models.JSONField()

    def __str__(self):
        return self.name