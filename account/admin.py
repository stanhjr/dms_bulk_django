from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']
    list_display = ('username', 'email', 'is_confirmed', 'dms_tokens', 'dollars')


admin.site.register(models.CustomUser, UserAdmin)
