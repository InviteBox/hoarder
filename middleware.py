import re
from datetime import datetime
import uuid

from django.conf import settings

from hoarder.models import RelVisitor
from hoarder import register_request_event
from hoarder.tasks import deduplicate, create_visitor, set_user

RE_HEADERS = re.compile('^HTTP_')


def _flatten_type(val):
    if isinstance(val, str) or isinstance(val, unicode) or isinstance(val, long) or isinstance(val, int):
        return val
    else:
        return unicode(val)

class LoggingMiddleware(object):

    def _get_headers(self, request):
        return dict((RE_HEADERS.sub('', header), value) for (header, value) 
                    in request.META.items() if header.startswith('HTTP_'))

    def process_request(self, request):
        if 'visitor_id' in request.session:
            visitor_id = request.session['visitor_id']
            if type(visitor_id) != str:
                visitor_id = str(visitor_id)
                request.session['visitor_id'] = visitor_id
            
        else:
            visitor_id = str(uuid.uuid4())
            create_visitor(visitor_id)
            request.session['visitor_id'] = visitor_id
        request_log = {'headers' : self._get_headers(request),
                       'path' : request.path,
                       'method' : request.method,
                       'get' : dict(request.GET)}
        register_request_event(request,
                               'request',
                               request_log)

            
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        args = [_flatten_type(x) for x in view_args]
        kwargs = dict([(x,_flatten_type(y)) for x,y in view_kwargs.items()])
        view = {'view' : view_func.__module__ + '.' + view_func.__name__ ,
                'args' : args,
                'kwargs' : kwargs}
        register_request_event(request, 'view', view)
        
        

class DeduplicationMiddleware(object):
    def process_request(self, request):
        visitor_id = request.session['visitor_id']
        if request.user.is_authenticated():
            try:
                rv = request.user.relvisitor
                if rv.visitor_id != visitor_id:
                    deduplicate.delay(visitor_id, rv.visitor_id)
                    request.session['visitor_id'] = rv.visitor_id
            except RelVisitor.DoesNotExist:
                RelVisitor.objects.create(user=request.user,
                                          visitor_id=visitor_id)
                set_user.delay(visitor_id,
                               request.user)
        
