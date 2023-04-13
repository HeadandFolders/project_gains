from django.db import models
from django.contrib.auth.models import User
from django.apps import apps #from stackoverflow 
from django.db.models import Sum #from another stackoverflow post https://stackoverflow.com/questions/56046688/how-to-get-the-sum-of-a-field-in-django
# Create your models here.
#personal observation: like in cpp the function order matters here(i.e when Hashtag was below Post there was a warning that Hashtag was not created or smthng?)

def get_avg_rating(url):
    Post = apps.get_model(app_label='WorkoutApp', model_name='Post')
    #Video = apps.get_model(app_label='WorkoutApp', model_name='Video')
    video_n =  Post.objects.filter(url = url).count() #* Task.DEFAULT_VALUE
    print(video_n)
    sum = Post.objects.filter(url=url).aggregate(sum_of_rating=Sum("rating"))
    return video_n/sum


class Hashtag(models.Model):
    hashtag = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.hashtag}"


class Video(models.Model):
    url = models.URLField()
   # ratings = models.ForeignKey(Post)
    #avgrating = models.IntegerField(null=True, blank=True, default=get_avg_rating(url))

    


class Post(models.Model):
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.ForeignKey(Video,on_delete=models.CASCADE) #ManyToOne because each post can have one video but each video has multiple people posting about it 
    hashtag = models.ManyToManyField(Hashtag) #because each post can have multiple tags and tags can be included in multiple posts
    opinion = models.CharField(max_length=200)
    rating = models.IntegerField() # same as url but i want it to be in Video so i can later calculate universal ranking of each individual video
    #comment_rating = models.IntegerField()
    #comment_opinio = models.CharField(max_length = 200)



