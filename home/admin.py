from django.contrib import admin

from home.models import FAQModel


class FAQModelAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


admin.site.register(FAQModel, FAQModelAdmin)
