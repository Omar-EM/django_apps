from django.forms import Form, CharField, BooleanField, EmailField
from django.forms.widgets import Textarea
from django.db.models import TextField


class BandContactForm(Form):
    subject = CharField(max_length=100)
    message = Textarea()
    sender = EmailField()
    cc_myself = BooleanField(required=False)
