from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "id",
        "type",
        "first_name",
        "last_name",
        "gender",
        "address",
        "is_staff",
        "is_superuser",
    ]
    list_filter = ["type", "is_superuser"]
    fieldsets = [
        (None, {"fields": ["id", "password"]}),
        ("Name", {"fields": ["type", "first_name", "last_name"]}),
        (
            "Additional Info",
            {
                "fields": [
                    "address",
                    "dob"
                ]
            },
        ),
        ("Permissions", {"fields": ["is_staff", "is_active", "is_superuser"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # add_fieldsets = [
    #     (
    #         None,
    #         {
    #             "classes": ["wide"],
    #             "fields": ["id", "password1", "password2"],
    #         },
    #     ),
    # ]
    search_fields = ["id"]
    ordering = ["id"]
    filter_horizontal = []


# Register your models here.
admin.site.register(User, UserAdmin)
