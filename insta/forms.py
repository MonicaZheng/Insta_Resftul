from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from insta.models import InstaUser, Post

# forms defined here handles user inputs

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = InstaUser
        fields = ('username', 'email', )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = InstaUser
        fields = ('username', 'email', )

# class PostPictureForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'image', ]