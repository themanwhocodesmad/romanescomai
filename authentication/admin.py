# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    list_display = ['username', 'first_name', 'last_name', 'role', 'service_center','cell_number' ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role','service_center','cell_number')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
