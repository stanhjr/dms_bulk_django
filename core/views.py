from django.views.generic import TemplateView


class RobotsTxtPageView(TemplateView):
    template_name = 'robots.txt'