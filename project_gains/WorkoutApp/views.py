from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.

tasks = ["foo", "bar", "baz"]
def index(request):
    context = {
    'tasks': tasks
    }
    template = loader.get_template('WorkoutApp/index.html')
    return HttpResponse(template.render(context, request))
