import os
import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


def get_file_path(instance, filename):
    return os.path.join(
        str(instance.owner.username),
        datetime.now().strftime("%Y-%m-%d"),
        filename
    )


class File(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(
        User,
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

    @property
    def owner_username(self):
        return os.path.basename(self.owner.username)

    @classmethod
    def model_field_exists(cls, field):
        try:
            cls._meta.get_field(field)
            return True
        except models.FieldDoesNotExist:
            return False

    class Meta:
        ordering = ['-created_at']


class ApiKey(models.Model):
    owner = models.OneToOneField(
        User,
        related_name='api_keys',
        on_delete=models.CASCADE,
        null=False,
    )
    api_key = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        default=uuid.uuid4().hex,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
