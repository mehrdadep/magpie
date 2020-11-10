import os
import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from magpie.core.helper import Helper


def get_file_path(instance, filename):
    return os.path.join(
        str(instance.consumer.name),
        datetime.now().strftime("%Y-%m-%d"),
        filename
    )


class Consumer(models.Model):
    name = models.CharField(
        max_length=512,
        null=False,
        blank=False,
        unique=True,
        default=Helper.generate_name,
    )
    token = models.CharField(
        max_length=512,
        null=False,
        blank=False,
        default=Helper.generate_token,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class File(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    consumer = models.ForeignKey(
        Consumer,
        related_name='files',
        on_delete=models.SET_NULL,
        null=True,
    )
    file_name = models.CharField(
        max_length=512,
        null=False,
        blank=False,
        default=uuid.uuid4().hex,
    )
    file = models.FileField(upload_to=get_file_path)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def model_field_exists(cls, field):
        try:
            cls._meta.get_field(field)
            return True
        except models.FieldDoesNotExist:
            return False

    class Meta:
        ordering = ['-created_at']



