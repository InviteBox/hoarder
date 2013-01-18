from datetime import datetime

from django.conf import settings
from django.template.loader import render_to_string

class GABackend(object):

    is_async = False

    def __init__(self, request=None):
        self.request = request

    def register_event(self,
                       event_type,
                       visitor_id,
                       when=None,
                       data={}):
        if not self.request:
            return 
        if event_type in ('request', 'view'):
            return
        if not hasattr(self.request, 'ga_events'):
            self.request.ga_events = []
        self.request.ga_events.append({'type' : event_type,
                                       'timestamp' : when,
                                       'visitor_id' : visitor_id,
                                       'data' : data})
                       
    def label_visitor(self, 
                      visitor_id,
                      label):
        pass

    def create_visitor(self,
                       visitor_id):
        pass

                      
    def deduplicate(self,
                    from_visitor_id,
                    to_visitor_id):
        pass

    def set_user(self,
                 visitor_id,
                 user):
        pass

    def get_tracking_code(self,
                          context):
        return render_to_string('hoarder/ga.html',
                                {'GA_PROPERTY_ID' : settings.GA_PROPERTY_ID},
                                context_instance=context)

