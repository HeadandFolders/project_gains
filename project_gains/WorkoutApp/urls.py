from django.urls import path
from . import views

app_name = "WorkoutApp" #this is app name for the urls;it helps uniquely identify all of the urls
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add")
]
