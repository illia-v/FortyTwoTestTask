from django.views.generic import TemplateView


class MessagesIndexView(TemplateView):
    template_name = 'messages/index.html'


class MessagesDetailView(TemplateView):
    template_name = 'messages/detail.html'
