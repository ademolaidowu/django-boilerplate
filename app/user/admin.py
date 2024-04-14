from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserOTP


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(BaseUserAdmin):
    """
    An abstract base class implementing a fully featured User Admin panel.
    """

    fieldsets = (
        (
            "User Information",
            {"fields": ("id", "email", "password", "is_confirmed", "last_login")},
        ),
        (
            "Record Information",
            {"fields": ("date_created", ("date_modified", "date_deleted"))},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "secret_keys",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "New User Information",
            {
                "fields": ("email", "password1", "password2"),
                "classes": (
                    "wide",
                    "extrapretty",
                ),
            },
        ),
    )

    list_display = (
        "email",
        "full_name",
        "is_confirmed",
        "is_active",
        "last_login",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_confirmed",
        "groups",
    )
    search_fields = ("email",)
    ordering = ("-date_created",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ("id", "last_login", "date_created", "date_modified", "date_deleted", "secret_keys")

    # inlines = [UserProfileInline]


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin model class for the User Profile model
    """

    list_display = ("user", "full_name", "type", "is_confirmed", "is_verified")
    list_filter = ("type", "is_confirmed", "is_verified")
    ordering = ("-date_created",)
    search_fields = ["user", "business_id"]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserOTP)
