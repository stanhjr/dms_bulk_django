from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect


class ConfirmRequiredMixin(AccessMixin):
    """
    Verify that current user confirm his account by email
    """

    dashboard_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        print(self.dashboard_url)
        if not request.user.is_confirmed:
            return redirect(self.dashboard_url)
        return super().dispatch(request, *args, **kwargs)
