from django.db import models
from django.contrib.auth.models import User,PermissionsMixin
# Create your models here.

class User(User,PermissionsMixin):
    def __init__(self):
        return self.first_name
