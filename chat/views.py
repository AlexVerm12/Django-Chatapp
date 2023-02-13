
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print("received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages':  chatMessages})


def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username= request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})


def register_view(request):
    if request.method == 'POST':
        print("received data " + request.POST['username'] + request.POST['password']+ request.POST['confirm_password'])
        if request.POST['username'] and request.POST['password'] == request.POST['confirm_password']:
            user = User.objects.create_user(username= request.POST['username'], password= request.POST['password'])
        else: 
            return render(request, 'auth/register.html', {'passwordNotIdent': True,})
    return render(request, 'auth/register.html')