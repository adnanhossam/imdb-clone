from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class User(models.Model):
    User.name = 'name'
    User.password = 'password'
    User.email = "email"
    User.phone_number = "phone_number"
    User.favorite_genre = "favorite_genre"
    
    
    