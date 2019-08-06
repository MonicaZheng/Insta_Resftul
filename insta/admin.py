from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from insta.forms import CustomUserChangeForm, CustomUserCreationForm
from insta.models import (Comment, InstaPost, InstaUser, Like, Post,
                          UserConnection)

# Register your models here.

class InstaUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'age',]
    model = InstaUser

class CommentInline(admin.StackedInline):
    model = Comment

class LikeInline(admin.StackedInline):
    model = Like

class InstaPostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
        LikeInline,
    ]

admin.site.register(Post)
admin.site.register(InstaPost, InstaPostAdmin)
admin.site.register(InstaUser, InstaUserAdmin)
admin.site.register(UserConnection)
admin.site.register(Comment)
admin.site.register(Like)
