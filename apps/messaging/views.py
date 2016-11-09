from django.views.generic import TemplateView


class MessagingIndexView(TemplateView):
    template_name = 'messaging/index.html'


class MessagingDetailView(TemplateView):
    template_name = 'messaging/detail.html'
