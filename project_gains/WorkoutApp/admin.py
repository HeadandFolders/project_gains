from django.contrib import admin
from .models import Video,Hashtag,Post,UserProfile,AccGroup
# Register your models here.
admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Video)
admin.site.register(UserProfile)
admin.site.register(AccGroup)
