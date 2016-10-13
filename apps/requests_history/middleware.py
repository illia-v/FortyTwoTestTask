from .models import Request


class RequestSavingMiddleware(object):
    """
    A middleware class which saves data about every request
    """
    def process_request(self, request):
        if request.is_ajax():
            return

        self.request = Request.objects.create(url=request.path,
                                              method=request.method)
