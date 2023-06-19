from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate ,logout, login

from .models import *
from blogs.models import *


def home(request):
    current_proj = Post.objects.all()
    return render (request,'test.html', {'current_proj':current_proj})


def contact(request):
    if(request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = str(request.POST.get('contact'))
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        try:	
            send_mail( 
                subject,
                'from:' +email + '\nname:'+ name +'\nphone:'+contact+'\nmessage:'+message,
                'pandeyprabhat583@gmail.com',
                ['paliwalap7@gmail.com', email],
                fail_silently=False,
                )
            messages.success(request, 'Mail Sent Successfully')
        except:
            messages.error(request, 'Mail Sent Failed! Some Error Occured')
    return render(request, 'contact-two.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    pass
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print('........',username, password)
        user= authenticate(username =username, password = password)
        if user==None:
            messages.error(request, 'Please Enter Correct Details')
            # return HttpResponse('enter correct details')
            # return render(request,'login.html')
        else:
            login(request, user)
            return redirect('/')
    return render(request,'login.html')

def signup(request):
    
    if request.method=='POST':
        name = request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        obj=User.objects.create_user(username=name , email=email, password=password)
        obj.save()
        return redirect('/login')
    return render(request,'signup.html')
    

def signof(request):
    logout(request)
    return redirect('/')

