import json

from django.http import HttpResponse
from django.utils.formats import date_format
from django.views.generic import ListView, View

from .models import Request


class RequestsHistoryView(ListView):
    model = Request
    queryset = model.objects.all().order_by('-id')[:10]
    context_object_name = 'requests'
    template_name = 'requests_history/requests_history.html'


class RequestsPullingView(View):
    """
    A view which pulls a client page with new requests on demand
    """
    def get(self, request, *args, **kwargs):
        last_request_id_on_page = int(request.GET['last_request_id'])

        # If a clients page is up to date
        if Request.objects.last().id == last_request_id_on_page:
            return HttpResponse('[]', content_type='application/json')

        new_requests = []
        for new_request in Request.objects\
                .filter(id__gt=last_request_id_on_page).order_by('id'):
            new_requests.append({
                'id': new_request.id,
                'url': new_request.url,
                'method': new_request.method,
                'timestamp': date_format(new_request.timestamp,
                                         'DATETIME_FORMAT')
            })

        return HttpResponse(json.dumps(new_requests),
                            content_type='application/json')
