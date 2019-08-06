from insta.models import Comment, InstaPost, InstaUser, Like
from rest_framework.serializers import ModelSerializer, StringRelatedField


class InstaUserSerializer(ModelSerializer):
    class Meta:
        model = InstaUser
        fields = ('id', 'username', 'profile_pic',)

class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = InstaUser
        fields = ('username', 'profile_pic',)

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'posted_on',)

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ('user',)

class InstaPostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)

    class Meta:
        fields = ('id', 'author', 'image', 'title', 'posted_on', 'comments', 'likes', )
        model = InstaPost

class MakeInstaPostSerializer(ModelSerializer):

    class Meta:
        fields = ('image', 'title',)
        model = InstaPost
