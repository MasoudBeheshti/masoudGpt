from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,HttpResponse

from django.conf import settings
import os
import openai
from .models import Chat
from .forms import *

# Create your views here

if settings.OPEN_API_KEY:
    openai.api_key = settings.OPEN_API_KEY
else:
    raise Exception('OpenAI API Key not found')


def ask_openai(message):
    query = openai.ChatCompletion.create(
        model = "gpt-4o-mini",
        n=1,
        stop=None,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a helpful assistant named Fati-GPT designed by Masoud Beheshti. remember your name and your designers name"},
            {"role": "user", "content": message},
        ]
    )
    response = query.get('choices')[0]['message']['content']
    return response


@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now)
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})



def register(request):
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('chatApp:login')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('chatApp:login')

@login_required
def delete_massages(request):
    chats=Chat.objects.filter(user=request.user)
    if chats.count()>0:
        chats.delete()
    return redirect('chatApp:chatbot')