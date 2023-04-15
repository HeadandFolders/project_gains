from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.template import loader
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages #django flash messages
from django.contrib.auth import login, authenticate
from .forms import NewHashtag, NewPostForm, NewVideo, LoginUser
from WorkoutApp.models import Video, Post, Hashtag
from django.utils import timezone
# Create your views here.

tasks = ["foo", "bar", "baz"]

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
"""   
def loginuser(request):
    context = {
        'form': LoginUser(request.POST)

    }
    #if request.user.is_authenticated:

    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render(context, request))
"""

def index(request):
    context = {
    'tasks': Post.objects.order_by('-pub_date')[:5],
    "formpost": NewPostForm(),
    
    }
    #if request.user.is_authenticated:

    template = loader.get_template('WorkoutApp/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def contribute(request):
    pass
    """
    if request.method == "POST" and request.is_ajax():
        form = NewPostForm(request.POST)
        if form.is_valid():
            url = request.POST['data']['url']
            v, created = Video.objects.get_or_create(url = url)
            v.save()
            posto = form.cleaned_data["opinion"]
            postr = form.cleaned_data["rating"]
            p = Post(opinion=posto, pub_date=timezone.now(), rating=postr, author= request.user, url= v)
            p.save()
            hashtag = request.cleaned_data["data"]["tag"]
            for i in hashtag:
                i,created = Hashtag.objects.get_or_create(hashtag = i)
                i.save()
                p.hashtag.add(i)
    """

#@login_required(login_url='add.html')
@login_required
def add(request):
    template = loader.get_template('WorkoutApp/add.html') 
    context = {
        "formurl": NewVideo(),
        "formpost": NewPostForm(),
        "formtag": NewHashtag()
    }
    if request.method == "POST":
        form = NewPostForm(request.POST)
        form2 = NewVideo(request.POST)
        form3 = NewHashtag(request.POST)
        if form.is_valid() and form2.is_valid() & form3.is_valid():
            url = form2.cleaned_data["url"]
            v, created = Video.objects.get_or_create(url = url)
            v.save()
            posto = form.cleaned_data["opinion"]
            postr = form.cleaned_data["rating"]
            p = Post(opinion=posto, pub_date=timezone.now(), rating=postr, author= request.user, url= v)
            p.save()
            hashtag = form3.cleaned_data["hashtag"]
            x = hashtag.split(" ")
            for i in x:
                i,created = Hashtag.objects.get_or_create(hashtag = i)
                i.save()
                p.hashtag.add(i)
            
            

            return HttpResponseRedirect(reverse("WorkoutApp:index"))
        else:
            return render(request, "WorkoutApp/add.html",{
                "formurl": NewVideo(),
                "formpost": NewPostForm(),
                "formtag": NewHashtag()
            })
    return HttpResponse(template.render(context, request))