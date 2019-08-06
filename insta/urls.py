"""insta app url Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from insta.views import (EditProfile, ExploreView, FollowerProfile,
                         FollowingProfile, IndexView, MakeInstaPost,
                         PostDetail, SignUp, UserProfile, addComment, addLike,
                         toggleFollow)

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),

    path('post', MakeInstaPost.as_view(), name='makepost'),

    path('auth/signup', SignUp.as_view(), name='signup'),

    path('profile/<int:pk>/', UserProfile.as_view(), name='profile'),

    path('post/<int:pk>/', PostDetail.as_view(), name='post'),

    path('togglefollow', toggleFollow, name='togglefollow'),

    path('like', addLike, name='addLike'),

    path('comment', addComment, name='addComment'),

    path('explore', ExploreView.as_view(), name='explore'),

    path('edit_profile/<int:pk>/', EditProfile.as_view(), name='editprofile'),

    path('follower/<int:pk>/', FollowerProfile.as_view(), name='follower'),

    path('following/<int:pk>/', FollowingProfile.as_view(), name='following'),
]
