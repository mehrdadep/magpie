import os
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
    file_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        User,
        related_name='files',
        on_delete=models.SET_NULL,
        null=True,
    )
    file = models.FileField(upload_to=get_file_path)


class UserToken(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='tokens',
        on_delete=models.CASCADE,
        null=False,
    )
    user_token = models.CharField(max_length=128, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
