from pymongo import Connection
from datetime import datetime

from django.conf import settings

connection = Connection(getattr(settings, 'HOARDER_MONGO_HOST', 'localhost'), 
                        getattr(settings, 'HOARDER_MONGO_PORT', 27017))

db = connection[getattr(settings, 'HOARDER_MONGO_DATABASE', 'hoarder')]

visitors = db.visitors
events = db.events


class MongoBackend(object):
    def get_context(self, request):
        return {}

    def register_event(self,
                       event_type,
                       visitor_id,
                       when=None,
                       data={}):
        if when is None:
            when = datetime.now()
        events.insert({'type' : event_type,
                       'timestamp' : when,
                       'visitor_id' : visitor_id,
                       'data' : data})
                       
    def label_visitor(self, 
                      visitor_id,
                      lablel):
        visitor = visitors.find_one({'id' : visitor_id})
        labels = visitor.get('labels', [])
        labels.append(label)
        visitor['labels'] = labels
        visitors.save(visitor)
                           

    def create_visitor(self,
                       visitor_id):
        visitors.insert({'id' : visitor_id})
                      
    def deduplicate(self,
                    from_visitor_id,
                    to_visitor_id):
        events.update({'visitor_id' : from_visitor_id },
                      {'$set' : {'visitor_id' : to_visitor_id }},
                      multi=True)
        old_visitor = visitors.find_one({'id' : from_visitor_id})
        new_visitor = visitors.find_one({'id' : to_visitor_id})
        labels = new_visitor.get('labels', [])
        labels += old_visitor.get('labels',[])
        new_visitor['labels'] = labels
        visitors.save(new_visitor)
        visitors.remove({'id': from_visitor_id})
        
    def set_user(self,
                 visitor_id,
                 user):
        pass

