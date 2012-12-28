from datetime import datetime

from hoarder.models import RelVisitor
from hoarder import tasks

def register_request_event(request, 
                           event_type, 
                           event_data={},
                           when=None):
    tasks.register_event.delay(event_type,
                               request.session['visitor_id'],
                               when=when,
                               data=event_data)
    

def register_user_event(user, 
                        event_type, 
                        event_data={},
                        when=None):
    try:
        visitor_id = user.relvisitor
    except RelVisitor.DoesNotExist:
        visitor_id = user.id
    tasks.register_event.delay(event_type,
                               visitor_id,
                               when=when,
                               data=event_data)
    


def label_visitor(request, label):
    tasks.label_visitor.delay(request.session['visitor_id'],
                              label)
