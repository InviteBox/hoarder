from hoarder.backends import get_backends

def tracking(request):
    ctx = {'visitor_id' : request.session['visitor_id']}
    for backend in get_backends():
        ctx.update(backend.get_context(request))
    return ctx
