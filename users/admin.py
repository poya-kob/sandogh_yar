from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("اطلاعات صندوق", {"fields": ("is_admin", "join_date")}),
    )

    list_display = ("username", "email", "is_admin", "join_date")
    list_filter = ("is_admin", "join_date")
