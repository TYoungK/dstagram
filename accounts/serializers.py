from rest_framework import serializers
from .models import User

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "tag",
            "name",
            "profile_pic",
            )
