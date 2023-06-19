from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
import json 
from chatv2.models import *
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username':request.user.username,
    })

@login_required
def test(request, room_name):
    return render(request, 'chat/chat2.html', {
        'room_name': mark_safe(json.dumps(room_name)),
        'username':mark_safe(json.dumps(request.user.username)),
    })


# Here's how it should goes 
# 1. To fetch all the chats list on the left [Chats]
# 2. When click on either of one we get the chats [fetch_message()]
# 3. To show the all the contacts list

# step 1
@login_required 
def test0(request):
    obj = Chat.objects.filter(participants__user = request.user)
    # you can also use get_object_or_404 it is very easy to use as well
    all_users = User.objects.all()
    chat_list = []
    for i in obj:
        if(i.participants.all()[0].user == request.user):
            chat_list.append([i.participants.all()[1], i.id])
        else:
            chat_list.append([i.participants.all()[0], i.id])
        print(i.participants.all()[0].user, i.id)
        
    print("............", all_users)
    # print(dir(obj))
    print(chat_list)
    return render(request, "chat/chat2.html", {
        "chat_list":chat_list, 
        'room_name': mark_safe(json.dumps("test")),
        'username':mark_safe(json.dumps(request.user.username)),
        'all_users':all_users,
        })

# step 2
def test1(request, id):
    obj = Chat.objects.filter(id = id).first()

    print(len(obj.participants.all()))

    for i in obj.messages.all():
        print(i.text)
    # print(obj.messages.all())
    return render(request, "chat/chat2.html")
    

def test2(request):
    contact = Contact.objects.get(user__username = "ap")
    obj = Chat.objects.filter(id = 2).first()
    msg = Message(contact = contact, text = "message from backend")
    msg.save()
    # obj.save()
    obj.messages.add(msg)
    obj.save()
    # obj.update()
    print(dir(obj))
    # print(obj.messages.all())
    
    return HttpResponse("done")

def create_chat(request, id):
    user = Contact.objects.get(user = request.user)
    friend = Contact.objects.get(user__id = id)

    if(Chat.objects.filter(participants = user).filter(participants= user)):
        return redirect('test0')
    obj = Chat()
    obj.save()
    obj.participants.add(user, friend)
    

    # Chat(participant = )
    return HttpResponse("done")


def chat_new(request):
    return render(request, 'chat/chat_new.html')