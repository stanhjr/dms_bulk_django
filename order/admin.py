from django.contrib import admin

from . import models


class OrderModelAdmin(admin.ModelAdmin):
    exclude = ('sending_start_at', 'send_messages_speed', 'completed')


admin.site.register(models.BoardModel)
admin.site.register(models.OrderModel, OrderModelAdmin)
admin.site.register(models.OrderCalcModel)
admin.site.register(models.Coupon)
