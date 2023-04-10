from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from django import forms
from django.forms import MultiWidget, TextInput 

# Create your views here.

tasks = ["foo", "bar", "baz"]

class NewPostForm(forms.Form):
    url = forms.URLField(label="workout_url")
    hashtag = forms.CharField(widget=TextInput(attrs={'placeholder': '#UpperBody'}), label="workout_hashtag")
    opinion = forms.CharField(label="workout_opinion")
    rating = forms.IntegerField(max_value=10, min_value=1, label="workout_rating")
    

def index(request):
    context = {
    'tasks': tasks
    }
    template = loader.get_template('WorkoutApp/index.html')
    return HttpResponse(template.render(context, request))

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