from django.conf import settings
from django.contrib.auth.models import User

from celery.decorators import task

from hoarder.backends import get_backends
    

@task
def create_visitor(visitor_id):
    for backend in get_backends():
        backend.create_visitor(visitor_id)


@task
def register_event(event_type,
                   visitor_id,
                   when,
                   data):    
    for backend in get_backends():
        backend.register_event(event_type,
                               visitor_id,
                               when,
                               data)


@task
def label_visitor(visitor_id,
                  label):    
    for backend in get_backends():
        backend.label_visitor(visitor_id,
                              label)


@task
def deduplicate(from_visitor_id, to_visitor_id):
    for backend in get_backends():
        backend.deduplicate(from_visitor_id,
                            to_visitor_id)

    return True


@task
def set_user(visitor_id, user_id):
    user = User.objects.get(id=user_id)
    for backend in get_backends():
        backend.set_user(visitor_id,
                         user)
    
