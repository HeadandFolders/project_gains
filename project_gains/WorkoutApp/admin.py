from django.contrib import admin
from .models import Video,Hashtag,Post
# Register your models here.
admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Video)
