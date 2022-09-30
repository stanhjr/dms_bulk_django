"""dms_bulk_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('important_info.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('account/', include('account.urls')),
    path('', include('order.urls')),
    path('blog/', include('blog.urls')),
    path('add-funds/', include('add_funds.urls')),
    path("stripe/", include('djstripe.urls', namespace='djstripe')),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path("payment/", include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

try:
    from not_found_page.views import NotFoundPageView
    urlpatterns.append(path('404/', NotFoundPageView.as_view()))
except ImportError:
    pass
