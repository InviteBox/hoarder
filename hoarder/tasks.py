from django.conf import settings
from django.contrib.auth.models import User

from celery.decorators import task

from hoarder.backends import get_async_backends
    

@task(ignore_result=True)
def create_visitor(visitor_id):
    for backend in get_async_backends():
        backend.create_visitor(visitor_id)


@task(ignore_result=True)
def register_event(event_type,
                   visitor_id,
                   when,
                   data):    
    for backend in get_async_backends():
        backend.register_event(event_type,
                               visitor_id,
                               when,
                               data)


@task(ignore_result=True)
def label_visitor(visitor_id,
                  label):    
    for backend in get_async_backends():
        backend.label_visitor(visitor_id,
                              label)


@task(ignore_result=True)
def deduplicate(from_visitor_id, to_visitor_id):
    for backend in get_async_backends():
        backend.deduplicate(from_visitor_id,
                            to_visitor_id)

    return True


@task(ignore_result=True)
def set_user(visitor_id, user_id):
    user = User.objects.get(id=user_id)
    for backend in get_async_backends():
        backend.set_user(visitor_id,
                         user)
    
