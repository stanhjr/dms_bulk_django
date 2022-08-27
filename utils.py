from django.views.generic.base import ContextMixin


class PopupCookiesContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cookies_policy_accepted'] = self.request.session.get('cookies_policy_accepted')

        return context