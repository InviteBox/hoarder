import time
import logging
from datetime import datetime

from django.conf import settings
from django.utils.importlib import import_module

_backends = None

def get_backends():
    global _backends
    if _backends is None:
        _backends = []
        for backend_path in settings.HOARDER_BACKENDS:
            be_module, be_classname = backend_path.rsplit('.', 1)
            mod = import_module(be_module)
            be_class = getattr(mod, be_classname)
            _backends.append(be_class())
    return _backends


        
    
        
class KISSMetricsBackend(object):

    def get_context(self, request):
        if not request.session.get('identify_kiss'):
            identify_kiss = True
            request.session['identify_kiss'] = True
        else:
            identify_kiss = False
        return {'identify_kiss' : identify_kiss,
                'KISSMETRICS_API_KEY' : settings.KISSMETRICS_API_KEY}


    def create_visitor(self,
                       visitor_id):
        pass

    def register_event(self,
                       event_type,
                       visitor_id,
                       when=None,
                       data={}):
        if event_type in ('request', 'view'):
            return
        from KISSmetrics import KM
        km = KM(settings.KISSMETRICS_API_KEY)
        km.identify(visitor_id)
        if when:
            data['_d'] = 1
            data['_t'] = int(time.mktime(when.timetuple()))
        km.record(event_type, data)
        

    def label_visitor(self,
                      visitor_id,
                      lablel):
        from KISSmetrics import KM
        km = KM(settings.KISSMETRICS_API_KEY)
        km.identify(visitor_id)
        km.set({'label':1})

    def deduplicate(self,
                    from_visitor_id,
                    to_visitor_id):
        from KISSmetrics import KM
        km = KM(settings.KISSMETRICS_API_KEY)
        km.alias(from_visitor_id, to_visitor_id)

    def set_user(self,
                 visitor_id,
                 user):
        from KISSmetrics import KM
        km = KM(settings.KISSMETRICS_API_KEY)
        km.identify(visitor_id)
        km.set({'user_id' : user.id, 'name' : user.get_full_name() })


class LogBackend(object):
    
    def __init__(self):
        self.logger = logging.getLogger('hoarder')

    def get_context(self, request):
        return {}

    def create_visitor(self,
                       visitor_id):
        self.logger.info('create_visitor(%s)'%repr(visitor_id))

    def label_visitor(self,
                       visitor_id):
        self.logger.info('label_visitor(%s, %s)'%(repr(visitor_id), repr(label)))
        
    def register_event(self,
                       event_type,
                       visitor_id,
                       when=None,
                       data={}):
    
        self.logger.info('register_event(%s,%s,%s,%s)'%(repr(event_type),
                                                        repr(visitor_id),
                                                        repr(when),
                                                        repr(data)))
    def deduplicate(self,
                    from_visitor_id,
                    to_visitor_id):
        self.logger.info('deduplicate(%s, %s)'%(repr(from_visitor_id),
                                               repr(to_visitor_id)))

    def set_user(self,
                 visitor_id,
                 user):
        self.logger.info('set_user(%s, %s)'%(repr(visitor_id),
                                             repr(user)))
        
