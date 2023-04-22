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
from .forms import NewHashtag, NewPostForm, NewVideo, LoginUser, ChangeProfile
from WorkoutApp.models import Video, Post, Hashtag, UserProfile, AccGroup
from django.utils import timezone
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.urls import resolve

# Create your views here.


def about(request):
    return render(request, 'WorkoutApp/about.html')

def create_user(request):
    template = loader.get_template('registration/signup.html')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            
            user_profile = UserProfile.objects.create(name=user)
            user_profile.save()
            login(request, user)
            #UserProfile.objects.create(name=user)
            template2 = loader.get_template('WorkoutApp/index.html')
            context = {
                'tasks': Post.objects.filter(PostCom=None),
                "formpost": NewPostForm(),
                'comments':Post.objects.all(),
                'avg_rating': Video.objects.values("url").annotate(average_rating=Avg("post__rating")),
                'accgroups': AccGroup.objects.all()
            }
            #return HttpResponse(template2.render(context,request))
            return HttpResponseRedirect(reverse("WorkoutApp:index"))
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

def profile(request, username=None):
        if username:
            print(username)
            user = get_object_or_404(User, username=username)
        else:
            user = request.user

        profile = get_object_or_404(UserProfile, name__username=user.username)
        print(profile.bio)
        args = {'user': user, 'tasks': Post.objects.filter(author__username= user.username),'image': profile, 'formpost': NewPostForm(), 'avg_rating': Video.objects.values("url").annotate(average_rating=Avg("post__rating"))}
        return render(request, 'WorkoutApp/profile.html', args)


def savepost(request, pk=None):
    post = get_object_or_404(Post, id=pk)
    userprofile = UserProfile.objects.get(name=request.user)
    userprofile.saved_posts.add(post)
    messages.success(request, 'Profile details updated.')
    return redirect('WorkoutApp:index')



def index(request):
    context = {
    'tasks': Post.objects.filter(PostCom=None),
    "formpost": NewPostForm(),
    'comments':Post.objects.all(),
    'avg_rating': Video.objects.values("url").annotate(average_rating=Avg("post__rating")),
    'accgroups': AccGroup.objects.all(),
    #'image': UserProfile.objects.get(name = request.user),
    'profile': UserProfile.objects.filter()
    }

    #video_id = Video.objects.values("url").url
    #print('http://youtube.com/embed/%s' % video_id[0])
    #if request.user.is_authenticated:
    #query = request.GET.get('search')
    #if query:
     #   context['object_list'] = Post.objects.filter(opinion__icontains=request.GET.get('search'))
     #https://stackoverflow.com/questions/69964943/how-to-put-button-value-to-database-django
    
    template = loader.get_template('WorkoutApp/index.html')
    return HttpResponse(template.render(context, request))


def search(request):
    context = {
    'tasks': Post.objects.filter(PostCom=None),
    "formpost": NewPostForm(),
    'comments':Post.objects.all(),
    'avg_rating': Video.objects.values("url").annotate(average_rating=Avg("post__rating")),
    }
    

    #if request.user.is_authenticated:
    query = request.GET.get('search')
    if query:
        context['object_list'] = Post.objects.filter(opinion__icontains=query)
    template = loader.get_template('WorkoutApp/search.html')
    return HttpResponse(template.render(context, request))


@login_required
def contribute(request):
    template = loader.get_template('WorkoutApp/index.html') 
    context = {
       # "formurl": NewVideo(),
        "formpost": NewPostForm(),
        #"formtag": NewHashtag()
    }
    if request.method == "POST":
        form = NewPostForm(request.POST)
        form_data = request.POST
        if form.is_valid():
            url = form_data["url_hidden"]
            v = Video.objects.get(url = url)
            #v.save()
            posto = form.cleaned_data["opinion"]
            postr = form.cleaned_data["rating"]
            p = Post(opinion=posto, pub_date=timezone.now(), rating=postr, author= request.user, url= v)
            p.save()
            hashtag = form_data["tag_hidden"]
            print(hashtag)
            x = hashtag.split(" ")
            for i in x:
                a = Hashtag.objects.get(hashtag=i)
                
                #if Hashtag.objects.filter(hashtag__hashatag=i).exists():
                print("exists")
                         #found.save()
                p.hashtag.add(a)
            originalpost_opinion = form_data["oposto_hidden"]
            o = Post.objects.get(opinion=originalpost_opinion)
            o.comments.add(p)
            o.save()
            

            return HttpResponseRedirect(reverse("WorkoutApp:index"))
        else:
            return render(request, "WorkoutApp/index.html",{
                "formpost": NewPostForm(),
                
            })
    return HttpResponse(template.render(context, request))

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