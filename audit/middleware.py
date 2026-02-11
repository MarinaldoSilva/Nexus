from threading import local

_threading_local = local()

def get_current_request():
    return getattr(_threading_local, 'request', None)

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _threading_local.request = request
        response = self.get_response(request)
        _threading_local.request = None
        return response