from django.contrib import admin
from django.contrib.auth.admin import Group, User
from .models import Profile, Sticky, Board#, Comment

# Unregister groups
admin.site.unregister(Group)

#combine profile and user info
class ProfileInline(admin.StackedInline):
    model = Profile

# extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

# Unregister initial user
admin.site.unregister(User)
# Reregister user with new model
admin.site.register(User, UserAdmin)

#register boards
admin.site.register(Board)

#register stickies
admin.site.register(Sticky)