from datetime import datetime
import uuid

from hoarder.models import RelVisitor
from hoarder import tasks
from hoarder.backends import get_sync_backends

def _get_visitor_id(request):
    if 'visitor_id' in request.session:
        visitor_id = request.session['visitor_id']
        if type(visitor_id) != str:
            visitor_id = str(visitor_id)
            request.session['visitor_id'] = visitor_id
    else:
        visitor_id = str(uuid.uuid4())
        tasks.create_visitor.delay(visitor_id)
        for b in get_sync_backends(request):
            b.create_visitor(visitor_id)
        request.session['visitor_id'] = visitor_id
    return visitor_id
    

def register_request_event(request, 
                           event_type, 
                           event_data={},
                           when=None):
    tasks.register_event.delay(event_type,
                               _get_visitor_id(request),
                               when=when,
                               data=event_data)
    for b in get_sync_backends(request):
        b.register_event(event_type,
                         _get_visitor_id(request),
                         when=when,
                         data=event_data)

    

def register_user_event(user, 
                        event_type, 
                        event_data={},
                        when=None):
    try:
        visitor_id = user.relvisitor.visitor_id
    except RelVisitor.DoesNotExist:
        visitor_id = user.id
    tasks.register_event.delay(event_type,
                               visitor_id,
                               when=when,
                               data=event_data)
    


def label_visitor(request, label):
    tasks.label_visitor.delay(_get_visitor_id(request),
                              label)
    for b in get_sync_backends(request):
        b.label_visitor(_get_visitor_id(request),
                        label)
        
