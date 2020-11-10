import uuid

from django.contrib import admin
from django.utils.translation import gettext as _

from file_server.apps.files.models import AuthToken
from file_server.apps.files.models import File
from file_server.core.helper import Helper


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
    list_per_page = 10

    def delete_queryset(self, request, queryset):
        for delete_object in queryset:
            delete_object.file.delete()
            delete_object.delete()


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['token', 'owner__username']
    list_display = (
        'owner',
        'token',
        'created_at',
        'updated_at',
    )
    readonly_fields = [
        'token',
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('Base Information', {
            'fields': (
                'owner',
                'token',
            ),
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at',
            ),
        }),
    )

    list_per_page = 10

    actions = ['update_token', ]

    def update_token(self, request, queryset):
        for token in queryset:
            token.token = Helper.generate_token()
            token.save()

        self.message_user(
            request,
            _("Token is updated successfully"),
        )

    update_token.short_description = _('Update token')
