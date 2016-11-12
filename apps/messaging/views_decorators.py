from django.http import HttpResponseBadRequest


def ajax_request(function):
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return function(request, *args, **kwargs)
    return wrapper
