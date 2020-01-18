from django.contrib import admin
from django.utils.translation import gettext as _

from file_server.apps.files.models import File
from file_server.apps.files.models import UserToken


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['service_name', 'method_name']
    list_display = (
        'file_id',
        'file',
        'owner',
        'created_at',
    )
    readonly_fields = [
        'created_at',
    ]


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['service_name', 'method_name']
    list_display = (
        'owner',
        'user_token',
        'created_at',
        'updated_at',
    )
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('Base Information', {
            'fields': (
                'owner',
                'user_token',
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

    actions = ['add_token', ]

    def add_token(self, request, queryset):
        self.message_user(
            request,
            _("Token is created/updated successfully"),
        )

    add_token.short_description = _('Add/Update token')
