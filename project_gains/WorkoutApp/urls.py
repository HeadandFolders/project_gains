from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "WorkoutApp" #this is app name for the urls;it helps uniquely identify all of the urls
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), #copy pasted code for template name thing
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.create_user, name='signup'),
    path('contribute/', views.contribute, name='contribute'),
    path('search/', views.search, name="search")
]
