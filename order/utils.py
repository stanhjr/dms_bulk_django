from django.contrib.auth.mixins import AccessMixin


class ConfirmRequiredMixin(AccessMixin):
    '''Verify that current user confirm his account by email'''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_confirmed:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
