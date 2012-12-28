from hoarder.backends import get_backends
from hoarder import _get_visitor_id

def tracking(request):
    ctx = {'visitor_id' : _get_visitor_id(request)}
    for backend in get_backends():
        ctx.update(backend.get_context(request))
    return ctx
