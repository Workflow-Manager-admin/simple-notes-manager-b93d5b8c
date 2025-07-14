from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    register,
    user_login,
    user_logout,
    UserDetailView,
    NoteViewSet,
)

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),

    # USER AUTH/MANAGEMENT
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('me/', UserDetailView.as_view(), name='user-detail'),

    # NOTES CRUD
    path('', include(router.urls)),
]
