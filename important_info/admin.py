from django.contrib import admin

from important_info.models import FAQModel


class FAQModelAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


admin.site.register(FAQModel, FAQModelAdmin)
