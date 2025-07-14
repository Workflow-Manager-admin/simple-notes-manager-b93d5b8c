from django.contrib import admin
from .models import User, Note

# PUBLIC_INTERFACE
class UserAdmin(admin.ModelAdmin):
    """Django admin model for User."""
    list_display = ("username", "email", "is_active", "is_staff", "date_joined")

# PUBLIC_INTERFACE
class NoteAdmin(admin.ModelAdmin):
    """Django admin model for Note."""
    list_display = ("title", "user", "created_at", "updated_at")
    search_fields = ("title", "user__username")
    readonly_fields = ("created_at", "updated_at")

admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)
