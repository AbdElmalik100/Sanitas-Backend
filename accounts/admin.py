from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class ManagingUsers(UserAdmin):
    add_fieldsets = (
            ('Main Information', {
                'classes':('wide',),
                'fields': ('first_name', 'last_name', 'username' ,'email', 'password1', 'password2'),
                }),
            ("Dates", {
                'fields': ('date_joined', 'last_login'),
            }),
            ('Permissions', {
                'fields': ('groups','user_permissions','is_staff', 'is_active', 'is_superuser')
            }),
            ('details', {
                'fields': ('gender', 'age')
            }),
        )
    fieldsets = (
            ('Main Information', {
                'classes':('wide',),
                'fields': ('first_name', 'last_name', 'username' ,'email', 'password'),
                }),
            ("Dates", {
                'fields': ('date_joined', 'last_login'),
            }),
            ('Permissions', {
                'fields': ('groups','user_permissions','is_staff', 'is_active', 'is_superuser')
            }),
            ('details', {
                'fields': ('gender', 'age', )
            }),
        )


admin.site.register(CustomUser, ManagingUsers)

admin.site.register(DiabetesNutrients)
admin.site.register(HypertensionNutrients)
admin.site.register(AllergyNutrients)