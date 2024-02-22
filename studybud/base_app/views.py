from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from django.contrib.auth.models import User     #OEM: django provides a User model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm      #OEM: django provides a User creation form
from .forms import RoomForm, UserForm

#OEM: Create a view

#rooms = [
#    {'id':1, 'name':'Lest learn python!'},
#    {'id':2, 'name':'Design with me'},
#    {'id':3, 'name':'Frontend devs'},
#]

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)        #OEM: This creates a session in the DB and the browser (see cookie/sessionid)
            return redirect('home')
        else:
            messages.error(request, "Username OR password does not exist")

    context = {'page': page}
    return render(request, "base_app/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()       #OEM: to be customized later

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)      #OEM commit=False so that we can get the user and 'clean' it
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration. ')

    return render(request, 'base_app/login_register.html', {'form': form})

def home(request):

    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    #rooms = Room.objects.all()      #--> to get all rows
    #rooms = Room.objects.get()      #--> to get one row
    #rooms = Room.objects.filter(topic__name__icontains=q)       #icontains: at least contains, i for case Insensitive, q ='' matches all queries
    rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    #rooms = Room.objects.exclude()
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    #room_messages = Message.objects.all().order_by('-created')  #To avoid adding order_by each time, we can add Meta class in the models 
    #room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))   #The msg has a room which has a topic which has a name

    context = {'rooms' : rooms, 'topics': topics, 
               "room_count": room_count, 'room_messages': room_messages}
    return render(request, 'base_app/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()       #message: refers to message table that is a a 'child' of room model, '_set' is added
    participants = room.participants.all()          #because it is a n:m relationship, no need of _set

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        #room_messages.add(message)
        return redirect('room_name', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base_app/room.html', context)

def profilePage(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'base_app/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)   #OEM: if it can't find it it will create it (and created==True)
        form = RoomForm(request.POST)
        #if form.is_valid():
        #    room = form.save(commit=False)  #OEM: commit=False, so that we can get the room instance before saving it in the db
        #    room.host = request.user        #We do this, because in the room creation form, the host field has been removed, so it is filled automatically before saving it in the db
        #    room.save()

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {"form": form, 'topics': topics}
    return render(request, 'base_app/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)          #OEM: pre-fill the Room to update by the existing data
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)   #OEM: if it can't find it it will create it (and created==True)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base_app/room_form.html', context) 
    

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST' :
        room.delete()
        return redirect('home')

    return render(request, 'base_app/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base_app/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base_app/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base_app/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base_app/activity.html', {'room_messages': room_messages})