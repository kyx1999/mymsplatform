from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'sex', 'create_time')
    list_display_links = ('name',)


admin.site.register(UserProfile, UserAdmin)
