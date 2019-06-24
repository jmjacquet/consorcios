from django.dispatch import receiver
from django.db.models.signals import pre_delete

from .models import *

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import post_save
