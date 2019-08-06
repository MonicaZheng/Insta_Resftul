from annoying.decorators import ajax_request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from insta.forms import CustomUserCreationForm
from insta.models import (Comment, InstaPost, InstaUser, Like, Post,
                          UserConnection)
# Django Rest Framework changes
from insta.serializers import (InstaPostSerializer, InstaUserSerializer,
                               MakeInstaPostSerializer, UpdateUserSerializer)
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)

# Create your views here.

class IndexView(ListAPIView):
    serializer_class = InstaPostSerializer

    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return InstaPost.objects.filter(author__in=following)

class ExploreView(ListAPIView):
    serializer_class = InstaPostSerializer

    def get_queryset(self):
        return InstaPost.objects.all().order_by('-posted_on')[:20]

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class MakeInstaPost(CreateAPIView):
    queryset = InstaPost.objects.all()
    serializer_class = MakeInstaPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(RetrieveAPIView):
    queryset = InstaPost.objects.all()
    serializer_class = InstaPostSerializer

class UserProfile(RetrieveAPIView):
    queryset = InstaUser.objects.all()
    serializer_class = InstaUserSerializer

class EditProfile(UpdateAPIView):
    queryset = InstaUser.objects.all()
    serializer_class = UpdateUserSerializer

class FollowerProfile(LoginRequiredMixin, ListView):
    model = InstaUser
    template_name = 'connections.html'
    login_url = 'login'

    def get_queryset(self):
        user_pk = self.kwargs['pk']
        this_user = InstaUser.objects.filter(pk=user_pk)
        followers = set()
        for conn in UserConnection.objects.filter(following__in=this_user):
            followers.add(conn.creator.pk)
        return InstaUser.objects.filter(pk__in=followers)

class FollowingProfile(LoginRequiredMixin, ListView):
    model = InstaUser
    template_name = 'connections.html'
    login_url = 'login'

    def get_queryset(self):
        following = set()
        connection_set = UserConnection.objects.filter(creator__pk=self.kwargs['pk'])

        for connection in connection_set:
            following.add(connection.following.pk)
        return InstaUser.objects.filter(pk__in=following)

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = InstaPost.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = InstaPost.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }
