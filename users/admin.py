from django.contrib import admin
from users.models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role','created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    list_select_related = ('user',)