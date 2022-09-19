from django.contrib import admin
from django.forms import Textarea
from django.db import models

from order.models import BoardModel
from order.models import OrderCalcModel
from order.models import OrderModel
from order.models import Coupon


class OrderModelAdmin(admin.ModelAdmin):
    search_fields = ['order_calc__user__username', 'order_calc__user__email']
    list_display = ('order_calc', 'scraping',
                    'filtering', 'sending', 'completed')
    exclude = ('sending_start_at', 'send_messages_speed', 'completed')

    class Media:
        js = ('js/js/jquery-3.6.0.min.js', 'js/js/admin/order-model.js')


class OrderCalcModelAdmin(admin.ModelAdmin):
    search_fields = ['user', 'social_network']
    list_display = ('social_network', 'amount', 'discount',
                    'total', 'created_at', 'user')


class BoardModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    class Media:
        css = {"all": ("css/custom_admin.css",)}


class CouponAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ('name', 'discount', 'left_to_use', 'uses')


admin.site.register(BoardModel, BoardModelAdmin)
admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderCalcModel, OrderCalcModelAdmin)
admin.site.register(Coupon, CouponAdmin)
