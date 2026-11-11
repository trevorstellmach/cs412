# dadjokes/serializers.py
# Converts django data models to a text representation to transmit over HTTP

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    """serializer for Joke model"""

    class Meta:
        model = Joke
        fields = ['text', 'name', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    """serializer for Picture model"""

    class Meta:
        model = Picture
        fields = ['image_url', 'name', 'timestamp']