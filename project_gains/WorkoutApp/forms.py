from django import forms
from django.forms import MultiWidget, TextInput  #for the placeholder

class NewPostForm(forms.Form):
    opinion = forms.CharField(label="workout_opinion")
    rating = forms.IntegerField(max_value=10, min_value=1, label="workout_rating")

class NewVideo(forms.Form):
    url = forms.URLField(label="workout_url")
  
class NewHashtag(forms.Form):
    hashtag = forms.CharField(widget=TextInput(attrs={'placeholder': '#UpperBody'}), label="workout_hashtag")
class LoginUser(forms.Form):
    user_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length = 50)

class ChangeProfile(forms.Form):
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(required=False)
    banner = forms.ImageField(required=False)