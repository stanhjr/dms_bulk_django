from django.contrib import admin

from . import models


class OrderModelAdmin(admin.ModelAdmin):
    search_fields = ['order_calc__user__username', 'order_calc__user__email']
    list_display = ('order_calc', 'scraping', 'filtering', 'sending', 'completed')
    exclude = ('sending_start_at', 'send_messages_speed', 'completed')


class OrderCalcModelAdmin(admin.ModelAdmin):
    search_fields = ['user', 'social_network']
    list_display = ('social_network', 'amount', 'discount', 'total', 'created_at', 'user')


class CouponAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ('name', 'discount', 'left_to_use', 'uses')


admin.site.register(models.BoardModel)
admin.site.register(models.OrderModel, OrderModelAdmin)
admin.site.register(models.OrderCalcModel, OrderCalcModelAdmin)
admin.site.register(models.Coupon, CouponAdmin)
