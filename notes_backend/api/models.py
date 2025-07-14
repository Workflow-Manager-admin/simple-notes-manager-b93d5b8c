from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# PUBLIC_INTERFACE
class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Username and email required. Password securely hashed.
    """
    # Optionally add extra fields, e.g. 'full_name' if needed.
    pass

# PUBLIC_INTERFACE
class Note(models.Model):
    """
    Note model representing an individual note created by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
