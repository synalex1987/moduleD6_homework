from django.db import models
#from author.models import Author
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    #subscribers = models.ManyToManyField(Author)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return self.name
