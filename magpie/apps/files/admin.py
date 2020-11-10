from django.contrib import admin
from django.utils.translation import gettext as _

from magpie.apps.files.models import Consumer
from magpie.apps.files.models import File
from magpie.core.helper import Helper


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['name', 'file_name']
    list_display = (
        'id',
        'consumer',
        'file',
        'file_name',
        'created_at',
    )
    readonly_fields = [
        'consumer',
        'created_at',
    ]
    list_per_page = 10

    def delete_queryset(self, request, queryset):
        for delete_object in queryset:
            delete_object.file.delete()
            delete_object.delete()


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['token', 'name']
    list_display = (
        'name',
        'token',
        'created_at',
        'updated_at',
    )
    readonly_fields = [
        'name',
        'token',
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('Base Information', {
            'fields': (
                'name',
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
