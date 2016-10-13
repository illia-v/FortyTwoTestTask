from django.views.generic import TemplateView


class HelloView(TemplateView):
    template_name = 'hello/index.html'
