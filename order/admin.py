from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from order.models import BoardModel, OrderCalcModel, OrderModel


class OrderModelAdmin(admin.ModelAdmin):
    exclude = ('sending_start_at', 'send_messages_speed', 'completed')


class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    class Media:
        css = {"all": ("css/custom_admin.css",)}


admin.site.register(BoardModel, YourModelAdmin)
admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderCalcModel)
