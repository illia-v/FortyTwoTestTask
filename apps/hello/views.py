import json
from StringIO import StringIO

from django import http
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .forms import HelloEditForm
from .models import PersonInfo


class HelloView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(HelloView, self).get_context_data(**kwargs)
        context['my_info'] = PersonInfo.objects.first()
        return context


class HelloEditView(View):
    def get(self, request, *args, **kwargs):
        person = PersonInfo.objects.first()
        form = HelloEditForm(initial=model_to_dict(person))
        photo_url = person.path_to_photo_from_media_root()
        return render(request, 'hello/edit.html', {'form': form,
                                                   'photo_url': photo_url})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            request_data = json.loads(request.body)

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
                                 {'photo': photo},
                                 instance=PersonInfo.objects.first())

            if form.is_valid():
                form.save()
                return http.HttpResponse(json.dumps({'status': 'success'}),
                                         content_type='application/json')
            else:
                return http.HttpResponseBadRequest('The form data is invalid')

        return http.HttpResponseForbidden('The form can be submited only via '
                                          'AJAX')
