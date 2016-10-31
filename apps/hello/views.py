import json
from StringIO import StringIO

from django import http
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .forms import HelloEditForm
from .models import PersonInfo
from general import signals

__all__ = ['signals']


class HelloView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(HelloView, self).get_context_data(**kwargs)
        context['my_info'] = PersonInfo.objects.first()
        return context


class HelloEditView(View):
    def get(self, request, *args, **kwargs):
        person = PersonInfo.objects.first()
        form = HelloEditForm(instance=person)
        return render(request, 'hello/edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            request_data = json.loads(request.body)

            encoded_photo = request_data.get('encoded_photo', None)
            if encoded_photo:
                # Photo is base64 encoded on front end because it is
                # transfered as JSON string via AJAX
                photo = InMemoryUploadedFile(
                    StringIO(request_data['encoded_photo'].decode('base64')),
                    field_name='photo',
                    name='illia.jpg',
                    content_type='image/jpg',
                    size=len(request_data['encoded_photo']),
                    charset='utf-8',
                )

            form = HelloEditForm(http.QueryDict(request_data['form_data']),
                                 {'photo': photo} if encoded_photo else None,
                                 instance=PersonInfo.objects.first())

            if form.is_valid():
                form.save()
                return http.HttpResponse(json.dumps({'status': 'success'}),
                                         content_type='application/json')
            else:
                return http.HttpResponseBadRequest('The form data is invalid')

        return http.HttpResponseForbidden('The form can be submited only via '
                                          'AJAX')
