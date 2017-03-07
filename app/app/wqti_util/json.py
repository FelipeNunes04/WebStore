from django.http import HttpResponse
from django.utils import simplejson as json


def _json_http_response(val):
    if val:
        r = json.dumps(val, indent=4)
    else:
        r = "{}"
    return HttpResponse(r, mimetype='text/javascript')

def to_json_response(f):
    def wrap(request, *args, **kwargs):
        result = f(request, *args, **kwargs)
        return _json_http_response(result)
        
    if callable(f):
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
    return _json_http_response(f)