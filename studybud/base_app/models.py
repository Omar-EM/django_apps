from django.db import models
from django.contrib.auth.models import User     #django provides a User model

# Create your models here.

#OEM: A topic can have multiple Rooms, whereas a Room can have only one Topic
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Room(models.Model):       #OEM: id gets created automatically
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    #OEM: null=True: means the field can be null in the db, blank=True: means the form can be empty
    description = models.TextField(null=True, blank=True)       
    #OEM: don't forget to run the migration after each modification of the model (python3 manage.py makemigrations   python3 manage.py migrate)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)    #OEM: See what is the role of related_name
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)   #field change only the first time##

    class Meta:
        ordering = ['-updated', '-created']     #This specifies the order in which the rows will appear (if we remove '-' it will be from the oldest to the newest)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #OEM: CASCADE: if the room gets deleted all the messages get deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)   #field change only the first time

    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self) -> str:
        return self.body[0:50]