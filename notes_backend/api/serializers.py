from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Note

# PUBLIC_INTERFACE
class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering new users."""

    password = serializers.CharField(write_only=True, min_length=8, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

# PUBLIC_INTERFACE
class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        data["user"] = user
        return data

# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object views."""
    class Meta:
        model = User
        fields = ("id", "username", "email")

# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """Serializer for note CRUD operations."""
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Note
        fields = ("id", "user", "title", "content", "created_at", "updated_at")
