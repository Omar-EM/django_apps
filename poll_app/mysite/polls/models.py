import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField("date published")   #OEM: "date published" is a human-readable name

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return  timezone.now() - datetime.timedelta(days=1) <= self.publication_date <= timezone.now()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    #Each choice is related to a single question (n:1)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)      #OEM: default value is set to 0

    def __str__(self):
        return self.choice_text