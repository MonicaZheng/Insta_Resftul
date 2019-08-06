from datetime import datetime
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField

# Create your models here.

class InstaUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality': 100},
        null=True,
        blank=True,
        )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def __str__(self):
        return self.username

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

class InstaPost(models.Model):
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, #foreign key is InstaUser
        blank=True,
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='insta_posts', # we can use author.posts to get all posts belong to this user
        )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        )
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title

    def get_like_count(self):
        return self.likes.count()

    def get_comment_count(self):
        return self.comments.count()

class Post(models.Model):
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, #foreign key is InstaUser
        blank=True,
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='posts', # we can use author.posts to get all posts belong to this user
        )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        )
    # default=datetime.now
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title

    def get_like_count(self):
        return self.likes.count()

    def get_comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(InstaPost, on_delete=models.CASCADE, related_name='comments',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment


class Like(models.Model):
    post = models.ForeignKey(InstaPost, on_delete=models.CASCADE, related_name='likes',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' ' + self.post.title
