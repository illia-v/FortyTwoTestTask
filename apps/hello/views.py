from django.views.generic import TemplateView

from .models import PersonInfo


class HelloView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(HelloView, self).get_context_data(**kwargs)
        context['my_info'] = PersonInfo.objects.first()
        return context


class HelloEditView(TemplateView):
    template_name = 'hello/edit.html'
