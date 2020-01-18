import uuid

from django.contrib import admin
from django.utils.translation import gettext as _

from file_server.apps.files.models import ApiKey
from file_server.apps.files.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['owner__username', 'file_name']
    list_display = (
        'file_id',
        'file',
        'file_name',
        'owner',
        'created_at',
    )
    readonly_fields = [
        'created_at',
    ]

    def delete_queryset(self, request, queryset):
        for delete_object in queryset:
            delete_object.file.delete()
            delete_object.delete()


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['api_key', 'owner__username']
    list_display = (
        'owner',
        'api_key',
        'created_at',
        'updated_at',
    )
    readonly_fields = [
        'api_key',
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('Base Information', {
            'fields': (
                'owner',
                'api_key',
            ),
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at',
            ),
        }),
    )

    list_per_page = 20

    actions = ['update_token', ]

    def update_token(self, request, queryset):
        for api_key in queryset:
            api_key.api_key = uuid.uuid4().hex
            api_key.save()

        self.message_user(
            request,
            _("Token is updated successfully"),
        )

    update_token.short_description = _('Update token')
