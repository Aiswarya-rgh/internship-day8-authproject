from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Employer,Candidate


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "phone",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone",
                    "role",
                    "is_verified",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # Add this
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


    readonly_fields = (
        "created_at",
        "updated_at",
    )

# Register Employer and Candidate models
admin.site.register(Employer)
admin.site.register(Candidate)