from django.contrib import admin

# Register your models here.
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "event_type",
        "action",
        "status",
        "user",
        "ip_address",
        "created_at",
    )

    list_filter = (
        "event_type",
        "status",
        "created_at",
    )

    search_fields = (
        "action",
        "description",
        "failure_reason",
        "ip_address",
        "user__username",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )