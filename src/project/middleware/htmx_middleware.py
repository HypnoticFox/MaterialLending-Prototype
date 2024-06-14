from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers

class HtmxHandlingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        
        if request.htmx:
            if "Vary" in response.headers:
                response["Vary"] = ",".join(response["Vary"], "HX-Request")
            else:
                response["Vary"] = "HX-Request"
            
            if(isinstance(response, HttpResponseRedirect)):
                response["HX-Redirect"] = response["Location"]
                del response["Location"]
        
        return response