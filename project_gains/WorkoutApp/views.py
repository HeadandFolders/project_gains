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
from django.utils import timezone, dateformat #maybe not needed
from calendar import HTMLCalendar
from datetime import datetime, date




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

#from IPython.display import HTML

# Based on https://stackoverflow.com/a/1458077/1639671
class HighlightedCalendar(HTMLCalendar):
    def __init__(self, highlight=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._highlight = highlight
    
    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        cssclass = self.cssclasses[weekday]
        if date.today() == date(self.year, self.month, day):
            cssclass += ' today'
        if day in self.workouts:
            cssclass += ' filled'
            
            return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
        return self.day_cell(cssclass, day)
    
    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

from itertools import groupby

from django.utils.html import conditional_escape as esc

class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                #body = ['<ul>']
                #for workout in self.workouts[day]:
                 #   body.append('<li>')
                  #  body.append('<a href="%s">' % workout.url.url)
                  #  body.append(esc(workout.rating))
                  #  body.append('</a></li>')
                #body.append('</ul>')
                #return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.pub_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


def profile(request, username=None):
        if username:
            print(username)
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        
        date_year = timezone.now().year
        date_month = timezone.now().month
        #cal = HTMLCalendar().formatmonth(date_year,date_month)

        userposts= Post.objects.filter(pub_date__year=date_year, 
                      pub_date__month=date_month, author__username = username)
        print(userposts)
        highlight = [1,2,3,4,5,6,7]
        #myset = set()
        #for dateobj in userposts:
            #for x,y in dateobj.items(): #https://stackoverflow.com/questions/64374956/print-values-of-dictionary-one-by-one
                #highlight.append(y.day)
         #       if y in highlight:
          #          print("its in here")
           #     else:
                    #highlight.append(int(y.day))
            #        print(type(int(y.day)))
        #print(myset)
        #highlight = list(myset)
        print(highlight)
        #days = datetime.strptime(userposts[1][1], '%d')
        #print(userposts)
        cal = WorkoutCalendar(userposts).formatmonth(date_year, date_month)
        #cal = HighlightedCalendar(highlight=highlight).formatmonth(date_month, date_year)
        profile = get_object_or_404(UserProfile, name__username=user.username)
        print(profile.bio)
        args = {
            'user': user,
            'cal': cal,
            'tasks': Post.objects.filter(author__username= user.username),
            'image': profile, 'formpost': NewPostForm(), 
            'avg_rating': Video.objects.values("url").annotate(average_rating=Avg("post__rating")),
            'daterange': userposts,
        }
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