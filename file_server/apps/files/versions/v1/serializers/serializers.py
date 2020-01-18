from rest_framework.serializers import ModelSerializer

from file_server.apps.files.models import File


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = (
            'owner',
            'file',
        )


class FilesSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = (
            'file_id',
            'file_name',
            'owner_username',
            'created_at',
        )
