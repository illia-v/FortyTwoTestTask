from django.views.generic import TemplateView


class RequestsHistoryView(TemplateView):
    template_name = 'requests_history/index.html'
