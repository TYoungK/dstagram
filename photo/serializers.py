from rest_framework import serializers
from .models import Photo, Follow

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
