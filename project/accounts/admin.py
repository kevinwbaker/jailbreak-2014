from django.contrib import admin
from django.contrib.auth.models import User

from accounts.models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
admin.site.register(User, UserAdmin)
