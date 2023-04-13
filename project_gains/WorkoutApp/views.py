from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.template import loader
from django import forms
from django.forms import MultiWidget, TextInput  #for the placeholder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages #django flash messages
from django.contrib.auth import login, authenticate
# Create your views here.

tasks = ["foo", "bar", "baz"]

class NewPostForm(forms.Form):
    url = forms.URLField(label="workout_url")
    hashtag = forms.CharField(widget=TextInput(attrs={'placeholder': '#UpperBody'}), label="workout_hashtag")
    opinion = forms.CharField(label="workout_opinion")
    rating = forms.IntegerField(max_value=10, min_value=1, label="workout_rating")

def create_user(request):
    template = loader.get_template('registration/signup.html')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            template2 = loader.get_template('WorkoutApp/index.html')
            context = {}
            return HttpResponse(template2.render(context,request))
            #return redirect('./WorkoutApp/index.html')
        else:
            return HttpResponse(template.render({'form':form}, request))
           # return render(request, 'registration/signup.html', {'form': form})
    else:
        messages.success(request, 'you are here.')
        form = UserCreationForm()
        context = {'form': form}
        template = loader.get_template('registration/signup.html')
        return HttpResponse(template.render(context, request))
    
class LoginUser(forms.Form):
    user_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length = 50)
def loginuser(request):
    context = {
        'form': LoginUser(request.POST)

    }
    #if request.user.is_authenticated:

    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render(context, request))


def index(request):
    context = {
    'tasks': tasks
    }
    #if request.user.is_authenticated:

    template = loader.get_template('WorkoutApp/index.html')
    return HttpResponse(template.render(context, request))



#@login_required(login_url='add.html')
@login_required
def add(request):
    template = loader.get_template('WorkoutApp/add.html') 
    context = {
        "form": NewPostForm()
    }
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            workout = form.cleaned_data["hashtag"]
            tasks.append(workout)
            return HttpResponseRedirect(reverse("WorkoutApp:index"))
        else:
            return render(request, "WorkoutApp/add.html",{
                "form": form
            })
    return HttpResponse(template.render(context, request))