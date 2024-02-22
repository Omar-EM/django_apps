from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"      #Create a form based on all fields of Room
        exclude = ['host' ,'participants']  #OEM: we exclude from the form, the following fields

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']