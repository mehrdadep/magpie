from rest_framework.serializers import ModelSerializer

from magpie.apps.files.models import File


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = (
            'id',
            'consumer',
            'file_name',
            'file',
            'created_at',
        )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'consumer': instance.consumer.name,
            'file_name': instance.file_name,
            'created_at': instance.created_at,
        }


class FilesSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = (
            'file_id',
            'file_name',
            'owner_username',
            'created_at',
        )
