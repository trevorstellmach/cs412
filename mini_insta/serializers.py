# mini_insta/serializers.py
# Converts django data models to a text representation to transmit over HTTP

from rest_framework import serializers
from .models import *
from django.utils import timezone

class ProfileSerializer(serializers.ModelSerializer):
    """serializer for Profile model"""
    num_followers = serializers.IntegerField(source='get_num_followers', read_only=True)
    num_following = serializers.IntegerField(source='get_num_following', read_only=True)
    num_posts = serializers.IntegerField(source='get_num_posts', read_only=True)

    class Meta:
        model = Profile
        fields = ['id',
                  'username',
                  'display_name',
                  'profile_image_url',
                  'bio_text',
                  'join_date',
                  'num_followers',
                  'num_following',
                  'num_posts']
        
class PhotoSerializer(serializers.ModelSerializer):
    """serializer for Photo model"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'url', 'timestamp']

    def get_url(self, obj):
        """retrieve image url"""
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    """serializer for Post model"""
    photos = PhotoSerializer(source='photo_set', many=True, read_only=True)
    author = serializers.CharField(source='profile.username', read_only=True)
    image_url = serializers.URLField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id','profile', 'author', 'caption', 'timestamp', 'photos', 'image_url']
        read_only_fields = ['id', 'profile', 'timestamp']

    def create(self, validated_data):
        """for when user creates a new post"""
        image_url = validated_data.pop('image_url', None)
        now = timezone.now()
        post = Post.objects.create(timestamp=now, **validated_data)
        if image_url:
            Photo.objects.create(post=post, image_url=image_url, timestamp=now)
        return post

class UserSerializer(serializers.ModelSerializer):
    """serializer for User model"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user