from django.contrib import admin

from important_info.models import PageModel
from important_info.models import SeoText
from important_info.models import SeoTitle


admin.site.register(PageModel)
admin.site.register(SeoText)
admin.site.register(SeoTitle)

