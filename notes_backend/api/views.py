from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
    NoteSerializer,
)

User = get_user_model()

@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
@api_view(['POST'])
def register(request):
    """Register a new user."""
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
@api_view(['POST'])
def user_login(request):
    """Log in a user and start session."""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
@api_view(['POST'])
def user_logout(request):
    """Log out the current user."""
    logout(request)
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
class UserDetailView(APIView):
    """Retrieve logged-in user's profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for notes. Auth required.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
