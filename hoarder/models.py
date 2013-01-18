from django.db import models
from django.contrib.auth.models import User


class RelVisitor(models.Model):
    user = models.OneToOneField(User)
    
    visitor_id = models.CharField(max_length=64)

