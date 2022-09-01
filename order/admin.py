from django.contrib import admin

from . import models


admin.site.register(models.BoardModel)
admin.site.register(models.OrderModel)
admin.site.register(models.OrderCalcModel)
