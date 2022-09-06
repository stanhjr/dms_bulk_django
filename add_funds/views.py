from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from utils import PopupCookiesContextMixin


class AddFundsPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'add_funds/add-funds.html'
